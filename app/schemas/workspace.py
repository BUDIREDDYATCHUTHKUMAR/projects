from pydantic import BaseModel,Field
from datetime import datetime
from typing import Optional

class WorkspaceBase(BaseModel):
    name:str=Field(...,min_length=1,max_length=100,description="the name of workspace",json_schema_extra={"example":"engineering team"})
    description:Optional[str]=Field(None,max_length=1000,description="optinal details regarding workspace",json_schema_extra={"example":"hub for backend services"})
class WorkspaceCreate(WorkspaceBase):
    pass 
class WorkspaceUpdate(BaseModel):
    name:Optional[str]=Field(None,min_length=1,max_length=100)
    description:Optional[str]=Field(None,max_length=1000)
class WorkspaceResponse(WorkspaceBase):
    id:int
    owner_id:int
    created_at:datetime
    updated_at:datetime
    model_config={
        "from_attributes":True
    }