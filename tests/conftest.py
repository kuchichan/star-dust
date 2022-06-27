# pylint: disable=redefined-outer-name

import asyncio
from asyncio.tasks import current_task
from typing import Any, AsyncGenerator, cast

import pytest
from fastapi.testclient import TestClient
from pydantic.networks import EmailStr, PostgresDsn
from sqlalchemy import text
from sqlalchemy.ext.asyncio.engine import AsyncEngine, create_async_engine
from sqlalchemy.ext.asyncio.scoping import async_scoped_session
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm.decl_api import registry
from sqlalchemy.orm.session import sessionmaker

from star_dust import crud
from star_dust.api.deps import get_current_user
from star_dust.core.config import settings
from star_dust.db.base import Base
from star_dust.db.session import get_db
from star_dust.main import app
from star_dust.schemas.user import UserCreate

AsyncScopedSession = async_scoped_session(
    sessionmaker(class_=AsyncSession), scopefunc=current_task
)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def create_test_db() -> AsyncGenerator[str, Any]:
    main_db_dsn = settings.database_dsn
    engine = create_async_engine(main_db_dsn)
    db_name = "test_db"

    async with engine.connect() as conn:
        await conn.execute(text("commit"))
        await conn.execute(text(f"create database {db_name}"))

    yield PostgresDsn.build(
        scheme=main_db_dsn.scheme,
        user=main_db_dsn.user,
        password=main_db_dsn.password,
        host=main_db_dsn.host,
        port=main_db_dsn.port,
        path=f"/{db_name}",
    )

    async with engine.connect() as conn:
        await conn.execute(text("commit"))
        await conn.execute(text(f"drop database {db_name}"))

    await engine.dispose()


@pytest.fixture(scope="session")
async def db_engine(create_test_db) -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(create_test_db)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="session")
async def db_tables(db_engine: AsyncEngine) -> AsyncGenerator[None, None]:
    DeclBase = cast(registry, Base)

    async with db_engine.begin() as conn:
        await conn.run_sync(DeclBase.metadata.create_all)  # pylint: disable=no-member

    yield

    async with db_engine.begin() as conn:
        await conn.run_sync(DeclBase.metadata.drop_all)  # pylint: disable=no-member


@pytest.fixture(scope="function")
async def db_session(
    db_engine: AsyncEngine, db_tables  # pylint: disable=unused-argument
) -> AsyncGenerator[AsyncSession, None]:
    conn = await db_engine.connect()
    transaction = await conn.begin()
    AsyncScopedSession.configure(bind=conn)

    yield AsyncScopedSession()

    await AsyncScopedSession.remove()
    await transaction.rollback()
    await conn.close()


@pytest.fixture(scope="function")
async def override_get_db(db_session):
    def wrap():
        try:
            yield db_session
        finally:
            pass

    return wrap


@pytest.fixture
async def override_get_current_user(db_session):
    user_in = UserCreate(
        email=EmailStr("user@example.com"),
        is_active=True,
        is_superuser=False,
        nickname="kuchi",
        password="hello",
    )
    user = await crud.user.create(session_db=db_session, obj_in=user_in)

    def override_get_current_user():
        return user

    return override_get_current_user


@pytest.fixture
def authorized_client(override_get_db, override_get_current_user):
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    client = TestClient(app)

    return client


@pytest.fixture
def exemplary_user():
    return UserCreate(
        email=EmailStr("pawel@example.com"),
        password="hello",
        is_active=True,
        is_superuser=True,
        nickname="kuchi",
    )
