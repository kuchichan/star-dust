from typing import Any

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio.session import AsyncSession

from star_dust import crud
from star_dust.core.security import create_access_token
from star_dust.db.session import get_db
from star_dust.schemas import token

router = APIRouter()


@router.post("/login/access-token", response_model=token.Token)
async def login_access_token(
    db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = await crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    return {
        "access_token": create_access_token(user.id),
        "token_type": "bearer",
    }
