from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from .models import base
from .database import engine, session_local



base.metadata.create_all(bind = engine)

app = FastAPI()


def get_db():
    db = session_local()

    try:
        yield db

    except Exception as e:
        print(e)

    finally:
        db.close()


@app.get("/test")
def testing(db: Session = Depends(get_db)):
    return {"status": "Successfull"}