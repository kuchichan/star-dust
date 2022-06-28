from decimal import Decimal

from pydantic import BaseModel


class AccountBase(BaseModel):
    minerals: int = 500
    dark_matter: int = 500
    dust_dollars: Decimal = Decimal("10000.00")


class AccountCreate(AccountBase):
    pass


class AccountUpdate(AccountBase):
    pass


class AcconutInDB(AccountBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
