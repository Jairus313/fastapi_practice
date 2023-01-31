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

@app.get("/posts/{id}")
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Post does not exist",
        )

    return {"post_detail": post}

@app.delete("/posts/{id}")
async def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if not post.first():
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Post does not exist"
        )

    post.delete(synchronize_session = False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
async def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if not post_query.first():
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Post does not exist"
        )

    post_query.update(post.dict(), synchronize_session= False)

    db.commit()

    return {"data": post_query.first()}