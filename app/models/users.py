from sqlalchemy import Column,Integer,String,Boolean,DateTime
from sqlalchemy.sql  import func
from app.database.database import Base

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    email=Column(String,unique=True,index=True,nullable=False)
    username=Column(String(100),nullable=False,index=True)
    hashed_password=Column(String(255),nullable=False)
    is_active=Column(Boolean,default=True,nullable=False)
    is_verified=Column(Boolean,default=False,nullable=False)
    created_at=Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    updated_at=Column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now(),nullable=False)