import pytest
from pydantic.networks import EmailStr
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from star_dust.crud.crud_account import account
from star_dust.crud.user import user
from star_dust.models.account import Account
from star_dust.schemas.account import AccountCreate
from star_dust.schemas.user import UserCreate


@pytest.mark.asyncio
async def test_create_account_with_owner_user(db_session: AsyncSession):
    user_from_api = UserCreate(
        email=EmailStr("pawel@example.com"),
        password="hello",
        is_active=True,
        is_superuser=True,
        nickname="kuchi",
    )
    result = await user.create(db_session, obj_in=user_from_api)

    account_from_api = AccountCreate()

    account_result = await account.create_with_owner(
        db_session, obj_in=account_from_api, owner_id=result.id
    )

    account_from_db = await db_session.execute(
        select(Account)
        .where(Account.id == account_result.id)
        .options(selectinload(Account.user))
    )

    [acc_result_from_db] = account_from_db.first()  # type: ignore

    assert acc_result_from_db.user == result
