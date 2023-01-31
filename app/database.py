from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


USERNAME = "postgres"
PASSWORD = "jairus313"
IP_ADDRESS = "localhost"
DATABASE_NAME = "fastapi"

SQLALCHEMY_DATABASE_URL = "postgresql://{}:{}@{}/{}".format(
                                                            USERNAME,
                                                            PASSWORD,
                                                            IP_ADDRESS,
                                                            DATABASE_NAME    
                                                        )

engine = create_engine(SQLALCHEMY_DATABASE_URL)

session_local = sessionmaker(autocommit = False, autoflush = False, bind = engine)

base = declarative_base()

def get_db():
    db = session_local()

    try:
        yield db

    except Exception as e:
        print(e)

    finally:
        db.close()