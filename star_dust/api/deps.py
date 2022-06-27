from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from jose import jwt
from jose.constants import ALGORITHMS
from jose.exceptions import JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio.session import AsyncSession

from star_dust import crud
from star_dust.core.config import settings
from star_dust.db.session import get_db
from star_dust.schemas.token import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.api_v1_str}/login/access-token"
)


async def get_current_user(
    db_session: AsyncSession = Depends(get_db), token: str = Depends(reusable_oauth2)
):
    try:
        decoded_token = jwt.decode(
            token, settings.secret_key, algorithms=[ALGORITHMS.HS256]
        )
        token_data = TokenPayload(**decoded_token)
    except (JWTError, ValidationError) as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials.",
        ) from exc

    user = await crud.user.get(db_session, id_=token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found."
        )

    return user
