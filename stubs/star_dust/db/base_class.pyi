from typing import Any
from sqlalchemy.orm.decl_api import DeclarativeMeta

class Base(metaclass=DeclarativeMeta):
    id: Any
    __abstract__ = True
