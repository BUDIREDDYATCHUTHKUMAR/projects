from pydantic import BaseModel, Field

class Note_create(BaseModel):
    # Enforces positive IDs greater than zero
    id: int = Field(..., gt=0, description="The unique ID of the note", example=1)
    
    # Enforces a minimum length of 1 character and maximum of 100 characters
    title: str = Field(..., min_length=1, max_length=100, description="The title of the note", example="Shopping List")
    
    # Enforces that content cannot be blank, but allows up to 2000 characters
    content: str = Field(..., min_length=1, max_length=2000, description="The detailed content of the note", example="Buy milk, eggs, and bread.")

class Note_update(BaseModel):
    # Same validation applied to updates to ensure consistency
    title: str = Field(..., min_length=1, max_length=100, example="Updated Shopping List")
    content: str = Field(..., min_length=1, max_length=2000, example="Buy milk and eggs only.")
