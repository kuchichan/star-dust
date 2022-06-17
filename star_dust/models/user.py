from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from star_dust.db.base_class import Base

if TYPE_CHECKING:
    from .account import Account


class User(Base):
    id: int = Column(Integer, primary_key=True, index=True)
    nickname: Optional[str] = Column(String, index=True)
    email: str = Column(String, unique=True, index=True, nullable=False)
    hashed_password: str = Column(String, index=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False)
    is_active: bool = Column(Boolean, default=False)

    account: "Account" = relationship("Account", back_populates="user", uselist=False)
