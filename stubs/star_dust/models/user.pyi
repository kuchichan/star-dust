from star_dust.db.base_class import Base
from typing import Optional

class User(Base):
    def __init__(
        self,
        id: Optional[str] = None,
        nickname: Optional[str] = None,
        email: str = None,
        hashed_password: str = None,
        is_superuser: Optional[bool] = None,
        is_active: Optional[bool] = None,
    ) -> None: ...
    @property
    def id(self) -> int: ...
    @property
    def nickname(self) -> str: ...
    @property
    def email(self) -> str: ...
    @property
    def hashed_password(self) -> str: ...
    @property
    def is_superuser(self) -> bool: ...
    @property
    def is_active(self) -> bool: ...
