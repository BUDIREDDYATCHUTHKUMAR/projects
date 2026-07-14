import logging
from fastapi import HTTPException,status
from app.repositories.user_repository import UserRepository
from app.models.users import User
from app.schemas.users import UserCreate,LoginRequest,TokenResponse
from app.core.security import hash_password,verify_password,create_access_token

logger=logging.getLogger("app.services.user_service")

class UserService:
    def __init__(self,user_repo:UserRepository):
        self.user_repo=user_repo
    def register_user(self,user_data:UserCreate)->User:
        logger.info(f"Registeration sequence initialized for email:{user_data.email}")
        existing_user=self.user_repo.get_by_email(user_data.email)
        if existing_user:
            logger.warning(f"Registeration fails due to email already existed:{user_data.email}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="a user with email already existed")
        hashed_pwd=hash_password(user_data.password)
        new_user=User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_pwd
        )
        try:
            saved_user=self.user_repo.create(new_user)
            logger.info(f"Registeration of user with email:{saved_user.id}")
            return saved_user
        except Exception as e:
            logger.error(f"Registeration fails due to unexcepted error:{str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="internal server error during registeration")
    def authenticate_user(self,login_data:LoginRequest)->TokenResponse:
        logger.info(f"Login autentication sequence initialized:{login_data.email}")
        user=self.user_repo.get_by_email(login_data.email)
        if not user:
            logger.warning(f"Login failed .Account not found:{login_data.email}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect email or password",headers={"www-Authenticate":"Bearer"})
        if not verify_password(login_data.password,user.hashed_password):
            logger.warning(f"Login failed due to incorrect password attempt:{login_data.email}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,headers={"www-Authenticate":"Bearer"})
        token_data={"sub":user.email,"user_id":user.id}
        jwt_token=create_access_token(token_data)
        logger.info(f"user account Id {user.id} found successfully authenticated.Token dispathced")
        return TokenResponse(access_token=jwt_token,token_type="bearer")