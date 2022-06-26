import pytest
from sqlalchemy.ext.asyncio.session import AsyncSession

from star_dust.crud.user import user
from star_dust.schemas.user import UserCreate


@pytest.mark.asyncio
async def test_user_crud_class_get_not_existed_user_returns_none(
    db_session: AsyncSession,
):
    result = await user.get(db_session, id_=100)

    assert result is None


@pytest.mark.asyncio
async def test_user_crud_class_create_and_get(
    db_session: AsyncSession, exemplary_user: UserCreate
):
    result = await user.create(db_session, obj_in=exemplary_user)

    result_get = await user.get(db_session, id_=result.id)

    assert result == result_get
