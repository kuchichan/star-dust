from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Body, Depends
from pydantic.networks import EmailStr
from sqlalchemy.ext.asyncio.session import AsyncSession

from star_dust.api.deps import get_current_user
from star_dust.crud.user import user as crud_user
from star_dust.db.session import get_db
from star_dust.schemas.user import User, UserCreate

router = APIRouter()


@router.post("/open-register", response_model=User)
async def open_registration(
    db: AsyncSession = Depends(get_db),
    password: str = Body(...),
    email: EmailStr = Body(...),
    nickname: str = Body(None),
):
    db_user = await crud_user.get_user_by_email(db, email)

    if db_user:
        raise HTTPException(
            status_code=400, detail="User with this email already exists."
        )

    user_in = UserCreate(email=email, nickname=nickname, password=password)
    user = await crud_user.create(db, obj_in=user_in)

    return user


@router.get("/me", response_model=User)
async def read_users_me(current_user=Depends(get_current_user)):
    return current_user
