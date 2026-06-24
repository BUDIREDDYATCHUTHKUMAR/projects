from fastapi import FastAPI
from app.routers.notes import router
from app.database import engine,Base
from app.models.noted import Note

app=FastAPI()
app.include_router(router)
Base.metadata.create_all(bind=engine)