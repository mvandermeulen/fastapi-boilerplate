from datetime import datetime
from datetime import timedelta
from typing import Annotated
from typing import Any
from typing import Union

import jwt
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from passlib.hash import pbkdf2_sha256
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.config import settings
from app.db import get_async_db
from app.models import User


ALGORITHM = "RS384"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_BASE_URL}/auth/login")


def create_token(
    subject: Union[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expire, "sub": subject}
    encoded_jwt = jwt.encode(
        to_encode, settings.PRIVATE_KEY_CONTENT, algorithm=ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str) -> Any:
    try:
        decoded_payload = jwt.decode(
            token, settings.PUBLIC_KEY_CONTENT, algorithms=[ALGORITHM]
        )
        return {"success": True, "payload": decoded_payload, "msg": None}
    except jwt.ExpiredSignatureError:
        return {"success": False, "payload": None, "msg": "Le jeton a expiré."}
    except jwt.InvalidTokenError:
        return {"success": False, "payload": None, "msg": "Le jeton est invalide."}


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_async_db),
) -> User | None:
    data = decode_token(token=token)
    revoked = await is_revoked(token=token)
    if revoked:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Revoked token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if data["success"]:
        user = await crud.user.get_db_obj_by_id(db=db, id=data["payload"]["sub"]["id"])
        if user:
            return user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def revok_token(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> Any:
    data = decode_token(token=token)
    if data["success"]:
        crud.redis_conn.create(f"revoked_token:{token}", token, data["payload"]["exp"])
        return {"message": "Successfully logout"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def is_revoked(token: str) -> bool:
    res = crud.redis_conn.exist(f"revoked_token:{token}")
    return res


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pbkdf2_sha256.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pbkdf2_sha256.hash(password)
