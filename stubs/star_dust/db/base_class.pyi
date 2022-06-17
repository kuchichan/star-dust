from sqlalchemy.orm.decl_api import DeclarativeMeta

class Base(metaclass=DeclarativeMeta):
    __abstract__ = True
