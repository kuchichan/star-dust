from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio.session import AsyncSession

from star_dust.crud.base import CRUDBase
from star_dust.models.account import Account
from star_dust.schemas.account import AccountCreate, AccountUpdate


class CRUDAccount(CRUDBase[Account, AccountCreate, AccountUpdate]):
    async def create_with_owner(
        self, session_db: AsyncSession, *, obj_in: AccountCreate, owner_id: int
    ) -> Account:
        object_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**object_in_data, user_id=owner_id)

        session_db.add(db_obj)

        await session_db.commit()
        await session_db.refresh(db_obj)

        return db_obj


account = CRUDAccount(Account)
