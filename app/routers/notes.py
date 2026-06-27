import sys
from typing import List,Annotated
from fastapi import APIRouter, HTTPException, Depends,status
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.schemas.note import Note_create,Note_update,NoteResponse,user_create,userResponse,Token
from app.models.noted import Note,User

from app.database  import sessionLocal
from app.core.security import hash_password,verify_password,create_token,SECRET_KEY, ALGORITHM


router=APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)) -> User:
    """Decodes the JWT token and fetches the current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user
#user register endpoints

@router.post("/register",response_model=userResponse,status_code=status.HTTP_201_CREATED)
def register_user(user_data:user_create,db:Session=Depends(get_db)):
    existing_user=db.query(User).filter(user_data.username==User.username).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="username already exists")
    hashed_pwd=hash_password(user_data.password)
    new_user=User(username=user_data.username,
                  email=user_data.email,
                  hashed_password=hashed_pwd
                  )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/token",response_model=Token)
def login_for_token(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user=db.query(User).filter(User.username==form_data.username).first()
    if not user or not verify_password(form_data.password,user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    access_token=create_token(data={"sub":user.username})
    return{ "access_token":access_token,"token_type":"bearer"}



@router.get("/search/notes/{q}",response_model=List[NoteResponse])
def search_note(q:str,db:Session=Depends(get_db),current_user: User = Depends(get_current_user)):
    return db.query(Note).filter(Note.user_id==current_user.id,Note.title.ilike(f"%{q}%")).all()
@router.post("/notes",response_model=NoteResponse)
def create_Note(note_in:Note_create,
                db:Session=Depends(get_db),
                current_user: User = Depends(get_current_user)):
    db_note=Note(title=note_in.title,content=note_in.content,user_id=current_user.id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

    
@router.get("/notes",response_model=List[NoteResponse])
def get_notes(db:Session=Depends(get_db),current_user: User = Depends(get_current_user)):
    return db.query(Note).filter(Note.user_id==current_user.id).all()
@router.get("/notes/{id}",response_model=NoteResponse)
def get_note(id:int,db:Session=Depends(get_db),current_user: User = Depends(get_current_user)):
    db_note=db.query(Note).filter(Note.id==id,Note.user_id==current_user.id).first()
    if not db_note:
         raise HTTPException(status_code=404,
                            detail="Note not found") 
    return db_note
@router.put("/notes/{id}",response_model=NoteResponse)
def update_note(id:int,note_data:Note_update,db:Session=Depends(get_db),current_user: User = Depends(get_current_user)):
    db_note=db.query(Note).filter(Note.id==id,Note.user_id==current_user.id).first()
    if not db_note:
         raise HTTPException(status_code=404, detail="Note not found")
    db_note.title=note_data.title
    db_note.content=note_data.content
    db.commit()
    db.refresh(db_note)
    return db_note
@router.delete("/notes/{id}",status_code=status.HTTP_200_OK)
def delete_note(id:int,db:Session=Depends(get_db),current_user: User = Depends(get_current_user)):
    db_note=db.query(Note).filter(Note.id==id,Note.user_id==current_user.id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(db_note)
    db.commit()
    return {"detail":"note sucessfully deleted"}

    