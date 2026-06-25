from fastapi import APIRouter, HTTPException, Depends
from app.schemas.note import Note_create,Note_update
from app.models.noted import Note
from sqlalchemy.orm import Session
from app.database  import sessionLocal
router=APIRouter()






def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/search/notes/{q}")
def search_note(q:str,db:Session=Depends(get_db)):
    return db.query(Note).filter(Note.title.ilike(f"%{q}%")).all()
@router.post("/notes")
def create_Note(note_in:Note_create,db:Session=Depends(get_db)):
    db_note=Note(title=note_in.title,content=note_in.content)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

    
@router.get("/notes")
def get_notes(db:Session=Depends(get_db)):
    return db.query(Note).all()
@router.get("/notes/{id}")
def get_note(id:int,db:Session=Depends(get_db)):
    db_note=db.query(Note).filter(Note.id==id).first()
    if not db_note:
         raise HTTPException(status_code=404,
                            detail="Note not found") 
    return db_note
@router.put("/notes/{id}")
def update_note(id:int,note_data:Note_update,db:Session=Depends(get_db)):
    db_note=db.query(Note).filter(Note.id==id).first()
    if not db_note:
         raise HTTPException(status_code=404, detail="Note not found")
    db_note.title=note_data.title
    db_note.content=note_data.content
    db.commit()
    db.refresh(db_note)
    return db_note
@router.delete("/notes/{id}")
def delete_note(id:int,db:Session=Depends(get_db)):
    db_note=db.query(Note).filter(Note.id==id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(db_note)
    db.commit()
    return {"detail":"note sucessfully deleted"}

    