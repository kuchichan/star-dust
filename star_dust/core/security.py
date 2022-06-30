from datetime import datetime, timedelta
from typing import Any, Union

from itsdangerous.url_safe import URLSafeTimedSerializer
from jose import jwt
from jose.constants import ALGORITHMS
from passlib.context import CryptContext

from star_dust.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
activation_serializer = URLSafeTimedSerializer(
    secret_key=settings.secret_key, salt="activation"
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_activation_token(subject: Union[str, Any]) -> Union[str, bytes]:
    return activation_serializer.dumps(subject)


def get_subject_from_activation_token(hash_: Union[str, bytes], max_age: int) -> str:
    return activation_serializer.loads(hash_, max_age=max_age)


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )

    to_encode = {"exp": expire, "sub": str(subject)}
    return jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHMS.HS256)
