from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.users import UserCreate,UserResponse,LoginRequest,TokenResponse
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from typing import Annotated
from app.models.users import User
from app.dependencies.auth  import get_current_user
from fastapi.security import OAuth2PasswordRequestForm

router=APIRouter(prefix="/auth",tags=["Authentication"])
@router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def register(user_in:UserCreate,db:Session=Depends(get_db)):
    user_repository=UserRepository(db)
    user_service=UserService(user_repository)
    return user_service.register_user(user_in)

@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login_with_json(login_in: LoginRequest, db: Session = Depends(get_db)):
    """Standard Login Endpoint. Accepts raw JSON body with email and password."""
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    return user_service.authenticate_user(login_in)

@router.post("/token",response_model=TokenResponse,status_code=status.HTTP_200_OK)
def login(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user_repository=UserRepository(db)
    login_payload=LoginRequest(email=form_data.username,password=form_data.password)
    user_service=UserService(user_repository)
    return user_service.authenticate_user(login_payload)
@router.get("/me",response_model=UserResponse,status_code=status.HTTP_200_OK)
def read_user_profile(current_user:Annotated[User,Depends(get_current_user)]):
    return current_user