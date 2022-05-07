import pytest
from sqlalchemy.ext.asyncio.engine import create_async_engine


@pytest.mark.asyncio
async def test_connection_to_test_db(create_test_db):
    engine = create_async_engine(create_test_db)
    conn = engine.connect()
    await conn.start()
    await conn.close()
    await engine.dispose()

    assert create_test_db.endswith("/test_db")
