from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from star_dust.core.security import get_password_hash, verify_password
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
        )

        session_db.add(db_obj)
        await session_db.commit()
        await session_db.refresh(db_obj)
        return db_obj

    async def get_user_by_email(
        self, session_db: AsyncSession, email: str
    ) -> Optional[User]:
        stmt = select(self.model).where(self.model.email == email)
        result = await session_db.execute(stmt)
        return result.scalars().first()

    async def authenticate(
        self, session_db: AsyncSession, *, email: str, password: str
    ) -> Optional[User]:
        db_user = await self.get_user_by_email(session_db, email)
        if not db_user:
            return None
        if not verify_password(password, db_user.hashed_password):
            return None
        return db_user


user = CRUDUser(User)
