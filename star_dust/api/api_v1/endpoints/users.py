from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Body, Depends
from pydantic.networks import EmailStr
from sqlalchemy.ext.asyncio.session import AsyncSession

from star_dust import crud
from star_dust.api.deps import get_current_user, get_mailing_method
from star_dust.core.config import settings
from star_dust.core.security import create_activation_token
from star_dust.db.session import get_db
from star_dust.mailing.utils import send_user_registration_link
from star_dust.schemas.user import User, UserCreate

router = APIRouter()


@router.post("/open-register", response_model=User)
async def open_registration(
    db: AsyncSession = Depends(get_db),
    send_email=Depends(get_mailing_method),
    password: str = Body(...),
    email: EmailStr = Body(...),
    nickname: str = Body(None),
):
    db_user = await crud.user.get_user_by_email(db, email)

    if db_user:
        raise HTTPException(
            status_code=400, detail="User with this email already exists."
        )

    user_in = UserCreate(email=email, nickname=nickname, password=password)
    user = await crud.user.create(db, obj_in=user_in)
    activation_token = create_activation_token(user.id)
    activation_link = f"{settings.server_host}/activate?token={activation_token!r}"
    send_user_registration_link(user, activation_link, send_email)

    return user


@router.get("/me", response_model=User)
async def read_users_me(current_user=Depends(get_current_user)):
    return current_user
