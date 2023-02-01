from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models, oauth2
from ..database import get_db



router = APIRouter(
    prefix= "/posts",
    tags= ["Posts"]
)


@router.get("/", response_model = List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    if not posts:
        raise HTTPException(
            status_code= status.HTTP_204_NO_CONTENT,
            detail= "No Posts were found"
        )

    return posts

@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.PostResponse)
async def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), 
    user_id: int = Depends(oauth2.get_current_user)):
    print(user_id)
    new_post = models.Post(
                        **post.dict()
                        )

    db.add(new_post)
    db.commit()

    db.refresh(new_post)     

    return new_post

@router.get("/{id}", response_model = schemas.PostResponse)
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Post does not exist",
        )

    return post

@router.delete("/{id}", response_model = schemas.PostResponse)
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

@router.put("/{id}", response_model = schemas.PostResponse)
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