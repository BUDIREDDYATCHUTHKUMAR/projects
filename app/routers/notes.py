from fastapi import APIRouter
from app.schemas.note import Note_create,Note_update
from fastapi import HTTPException
router=APIRouter()
notes=[]
@router.get("/")
def home():
    return {"message":"notes api"}

@router.get("/search/notes")
def search_note(q:str):
    result=[]
    for note in notes:
        if q.lower() in note.title.lower():
            result.append(note)
    return result
@router.post("/notes")
def create_Note(note:Note_create):
    notes.append(note)
    return note
@router.get("/notes")
def get_notes():
    return notes
@router.get("/notes/{id}")
def get_note(id:int):
    for note in notes:
        if note.id==id:
            return note
   
    raise HTTPException(status_code=404,
                            detail="Note not found") 
@router.put("/notes/{id}")
def update_note(id:int,note_data:Note_update):
    for note in notes:
        if note.id==id:
            note.title=note_data.title
            note.content=note_data.content
            return note
    raise HTTPException(status_code=404, detail="Note not found")
@router.delete("/notes/{id}")
def delete_note(id:int):
    for note in notes:
        if note.id==id:
            notes.remove(note)
            return {"detail":"note successfully deleted","remaining notes":notes}
    raise HTTPException(status_code=404, detail="Note not found")

    