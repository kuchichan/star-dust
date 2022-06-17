from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Numeric

from star_dust.db.base_class import Base

if TYPE_CHECKING:
    from .user import User


class Account(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    minerals = Column(Integer)
    dark_matter = Column(Integer)
    dust_dollars = Column(Numeric(precision=2))

    user: "User" = relationship("User", back_populates="account")  # type: ignore
