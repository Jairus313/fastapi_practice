from fastapi import FastAPI, Response, status, HTTPException

from pydantic import BaseModel
from typing import Optional

import psycopg2, logging, time
from psycopg2.extras import RealDictCursor



app = FastAPI()

logging = logging.getLogger("main")

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