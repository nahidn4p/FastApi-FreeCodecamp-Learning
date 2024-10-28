
import psycopg2
import time
from typing import List, Optional
from fastapi import *
from fastapi.params import Body
import psycopg2.extras
from pydantic import BaseModel
from . import schemas
from random import randrange

#from psycopg.rows import dict_row
from . import models,utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import post,user

models.Base.metadata.create_all(bind=engine)
while True:
    try:
        conn=psycopg2.connect(host='localhost',dbname='fastapi',user="Nahid.Hasan",password="postgres",
                             cursor_factory=psycopg2.extras.RealDictCursor)
        cursor=conn.cursor()
        print("Database Connection Successfull!")
        break
    except Exception as error:
        print("Connection Unsuccessfull")
        print("Error:",error)
        time.sleep(2)


app=FastAPI()


app.include_router(post.router)
app.include_router(user.router)