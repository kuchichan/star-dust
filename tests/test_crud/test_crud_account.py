import pytest
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from star_dust import crud
from star_dust.crud.crud_account import account
from star_dust.models.account import Account
from star_dust.schemas.account import AccountCreate
from star_dust.schemas.user import UserCreate


@pytest.mark.asyncio
async def test_create_account_with_owner_user(
    db_session: AsyncSession, exemplary_user: UserCreate
):
    result = await crud.user.create(db_session, obj_in=exemplary_user)

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
