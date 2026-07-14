from sqlalchemy import Column,Integer,String,ForeignKey,DateTime,Text
from sqlalchemy.sql  import func
from sqlalchemy.orm import relationship
from app.database.database import Base

class Workspace(Base):
    __tablename__="workspaces"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(100),index=True,nullable=False)
    description=Column(Text,nullable=True)
    owner_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    
    created_at=Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    updated_at=Column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now(),nullable=False)
    owner=relationship("User",back_populates="workspaces")