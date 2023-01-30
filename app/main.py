from fastapi import FastAPI, Response, status, HTTPException

from pydantic import BaseModel

import psycopg2, time
from psycopg2.extras import RealDictCursor



app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(
            host = "localhost",
            database = "fastapi",
            user = "postgres",
            password = "jairus@313",
            cursor_factory = RealDictCursor
        )

        cursor = conn.cursor()

        print("Database connection was successfull.")

        break

    except Exception as e:
        print("Database connection error: {}".format(str(e)))

        time.sleep(10)


class post(BaseModel):
    title: str
    content: str
    published: bool = True


@app.get("/")
async def root():
    return {"message": "FastAPI, Hello World"}

@app.get("/posts")
async def get_posts():
    cursor.execute(
        """
            SELECT * FROM posts;
        """
    )

    posts = cursor.fetchall()

    return {"data": posts}

@app.post("/posts", status_code = status.HTTP_201_CREATED)
async def create_posts(post: post):
    cursor.execute(
        """
            INSERT INTO 
                posts (title, content, published)
            VALUES
                (%s, %s, %s)
            RETURNING
                *;
        """,
        (post.title, post.content, post.published)
    )

    new_post = cursor.fetchone()

    conn.commit()

    return {"data": new_post}