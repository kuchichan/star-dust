import pytest
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import select

from star_dust.models.user import User


@pytest.mark.asyncio
async def test_user_table_connection(db_session: AsyncSession):
    user = User(
        id=1, nickname="hello", email="hehe@example.com", hashed_password="hehe"
    )  # type: ignore

    async with db_session.begin():
        db_session.add(user)
        await db_session.commit()

    stmt = select(User).where(User.id == 1)  # type: ignore
    result = await db_session.execute(stmt)
    db_user = result.first()

    assert db_user is not None
    assert db_user[0] == user
