from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas
from .database import engine, get_db
from .utils import hash



models.base.metadata.create_all(bind = engine)

app = FastAPI()


@app.get("/")
async def root():
    return "Server is up"

@app.get("/posts", response_model = List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    if not posts:
        raise HTTPException(
            status_code= status.HTTP_204_NO_CONTENT,
            detail= "No Posts were found"
        )

    return posts

@app.post("/posts", status_code = status.HTTP_201_CREATED, response_model = schemas.PostResponse)
async def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(
                        **post.dict()
                        )

    db.add(new_post)
    db.commit()

    db.refresh(new_post)     

    return new_post

@app.get("/posts/{id}", response_model = schemas.PostResponse)
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Post does not exist",
        )

    return post

@app.delete("/posts/{id}", response_model = schemas.PostResponse)
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

@app.put("/posts/{id}", response_model = schemas.PostResponse)
async def update_post(id: int, post: schemas.PostBase, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if not post_query.first():
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Post does not exist"
        )

    post_query.update(post.dict(), synchronize_session= False)

    db.commit()

    return post_query.first()

@app.post("/users", status_code = status.HTTP_201_CREATED, response_model= schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash(user.password)
    user.password = hashed_password

    new_user = models.User(
                        **user.dict()
                        )

    db.add(new_user)
    db.commit()

    db.refresh(new_user)     

    return new_user

@app.get("/users/{id}", response_model= schemas.UserResponse)
async def get_post(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User does not exist",
        )

    return user