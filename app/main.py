from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from .models import base
from .database import engine, get_db



base.metadata.create_all(bind = engine)

app = FastAPI()


@app.get("/test")
def testing(db: Session = Depends(get_db)):
    return {"status": "Successfull"}