from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from . import models
from .database import engine, get_db



models.base.metadata.create_all(bind = engine)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True


@app.get("/")
async def root():
    return {"message": "FastAPI, Hello World"}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    if not posts:
        raise HTTPException(
            status_code= status.HTTP_204_NO_CONTENT,
            detail= "No Posts were found"
        )

    return {"data": posts}

@app.post("/posts", status_code = status.HTTP_201_CREATED)
async def create_posts(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(
                        **post.dict()
                        )

    db.add(new_post)
    db.commit()

    db.refresh(new_post)     

    return {"data": new_post}