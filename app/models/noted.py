from sqlalchemy import Column,Integer,String,Text,Boolean,ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Note(Base):
    __tablename__="notes"
    id = Column(Integer, primary_key=True, index=True)
    title=Column(String(255))
    content=Column(Text)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User", back_populates="notes")
class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String,unique=True,index=True,nullable=False)
    email=Column(String,unique=True,index=True,nullable=False)
    hashed_password=Column(String,nullable=False)
    is_active=Column(Boolean,default=True)
    notes = relationship("Note", back_populates="owner", cascade="all, delete-orphan")