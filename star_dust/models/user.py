from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Identity, Integer, String
from sqlalchemy.orm import relationship

from star_dust.db.base_class import Base

if TYPE_CHECKING:
    from .account import Account


class User(Base):
    id = Column(Integer, Identity(), primary_key=True, index=True)
    nickname = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, index=True, nullable=False)
    is_superuser = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)

    account: "Account" = relationship("Account", back_populates="user", uselist=False)
