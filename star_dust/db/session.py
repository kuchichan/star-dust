from asyncio import current_task
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_scoped_session,
)
from sqlalchemy.orm import sessionmaker

from ..core.config import settings

engine = create_async_engine(settings.database_dsn)
async_session_factory = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)
AsyncScopedSession = async_scoped_session(async_session_factory, scopefunc=current_task)


@asynccontextmanager
async def get_connection():
    session = AsyncScopedSession()
    try:
        yield session
    finally:
        await session.remove()
