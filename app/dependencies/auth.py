import logging
from typing import Annotated
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt,JWTError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.database.session import get_db
from app.models.users  import User
from app.repositories.user_repository import UserRepository

logger=logging.getLogger("app.dependencies.auth")
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")
async def get_current_user(token:Annotated[str,Depends(oauth2_scheme)],db:Session=Depends(get_db))->User:
    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials.please login again",
        headers={"www-Authenticate":"Bearer"}
        )
    try:
        payload=jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        email:str=payload.get("sub")
        user_id:int=payload.get("user_id")
        if email is None or user_id is None:
            logger.warning("JWT token payload data matrix context is missing 'sub' or 'user_id' claims")
            return credentials_exception
    except JWTError as e:
        logging.warning(f"cryptographic validation failed for requested signature token:{str(e)}")
        return credentials_exception
    user_repository=UserRepository(db)
    user=user_repository.get_by_id(user_id)
    if user is None:
        logger.waring(f"JWT token maps to user_id{user_id} ,but this account not exists")
    if not user.is_active:
        logger.warning(f"Authenticated access blocked user accound Id{user_id}is currently due to inactive. ")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="this user account is deactivated")
    return user