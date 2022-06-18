from asyncio import current_task
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from ..core.config import settings

engine = create_async_engine(settings.database_dsn)
async_session_factory = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
AsyncScopedSession = async_scoped_session(async_session_factory, scopefunc=current_task)


async def get_db() -> AsyncGenerator:
    session = AsyncScopedSession()
    try:
        yield session
    except:
        await session.rollback()
        raise
    finally:
        await session.close()
