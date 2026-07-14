from pydantic import BaseModel,EmailStr,Field
from datetime import datetime

class UserBase(BaseModel):
    email:EmailStr
    username:str=Field(...,min_length=3,max_length=50)
class UserCreate(UserBase):
    password:str=Field(...,min_length=8,max_lengt=100)
class UserResponse(UserBase):
    id:int
    is_active:bool
    is_verified:bool
    created_at:datetime
    updated_at:datetime
    model_config={
        "from_attributes":True
    }
class LoginRequest(BaseModel):
    email:EmailStr
    password:str
class TokenResponse(BaseModel):
    access_token:str
    token_type:str="bearer"