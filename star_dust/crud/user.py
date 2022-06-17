from sqlalchemy.ext.asyncio import AsyncSession

from star_dust.core.security import get_password_hash
from star_dust.crud.base import CRUDBase
from star_dust.models.user import User
from star_dust.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def create(self, session_db: AsyncSession, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            nickname=obj_in.nickname,
            is_superuser=obj_in.is_superuser,
        )  # type: ignore
        session_db.add(db_obj)
        await session_db.commit()
        await session_db.refresh(db_obj)
        return db_obj


user = CRUDUser(User)
