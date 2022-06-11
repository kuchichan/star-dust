from typing import Any, AsyncGenerator

import pytest
from pydantic.networks import PostgresDsn
from sqlalchemy import text
from sqlalchemy.ext.asyncio.engine import create_async_engine

from star_dust.core.config import settings


@pytest.fixture
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
