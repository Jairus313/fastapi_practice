from fastapi import FastAPI, Response, status, HTTPException

from pydantic import BaseModel
from typing import Optional


class post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


app = FastAPI()

my_posts = [
    {
        "title": "post 1",
        "content": "post 1 content",
        "id": 1
    },
    {
        "title": "post 2",
        "content": "post 2 content",
        "id": 2 
    }
]

@app.get("/")
async def root():
    return {"message": "FastAPI, Hello World"}

# for references
# @app.post("/posts")
# async def get_posts(payload: dict = Body(...)):
#     return {"message": "a: {}, b: {}".format(payload['a'], payload['b'])}

@app.get("/posts")
async def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code = status.HTTP_201_CREATED)
async def create_posts(payload: post):
    payload = payload.dict()
    payload["id"] = len(my_posts) + 1

    my_posts.append(payload)

    return {"data": payload}

@app.get("/posts/{id}")
async def get_post(id: int):
    # response_data = None

    if len(my_posts) >= (id):
        return {"post_detail": my_posts[(id - 1)]}
    
    else:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # response_data = {"message": "post not found"}

        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Post deos not exist"
        )