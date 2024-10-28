
import psycopg2
import time
from typing import Optional
from fastapi import *
from fastapi.params import Body
import psycopg2.extras
from pydantic import BaseModel
from random import randrange
#from psycopg.rows import dict_row
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

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


class Post(BaseModel):
    title:str
    content:str
    published:bool=True
    # rating:Optional[int]=None

my_posts=[{"id":1,"title": "first post","content": "This is my first post"},{"id":2,"title": "second post","content": "This is my second post"},{"id":3,"title": "third post","content": "This is my third post"}]

def find_post(id):
    for p in my_posts:
        if p["id"]==id:
            return p
def find_index(id):
    for i,p in enumerate(my_posts):
        if p["id"]==id:
            return i
@app.get("/post/latest") 
def get_latest_post():
    post=my_posts[len(my_posts)-1]
    return {"Latest_Post":post}

@app.get("/sqlalchemy")
def alchemy_check(db: Session =  Depends(get_db)):
    posts=db.query(models.Post).all()
    return {"data":posts}


@app.get("/")
def root():
    return {"message": "Welcome"}

@app.get("/post")
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    data=cursor.fetchall()
    return {"data":data}

@app.post("/post/createpost",status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """, 
                   (post.title,post.content,post.published))
    new_post=cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.get("/post/{id}") 
def get_post(id:int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    post=cursor.fetchone()
    #post=find_post(id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} Not found")
    return {"Success": f"Here is your post {id}: {post}"}

@app.delete("/post/{id}",status_code=status.HTTP_204_NO_CONTENT)
def del_post(id:int):
    cursor.execute(""" DELETE FROM posts WHERE id= %s RETURNING *""", (str(id),))
    deleted_post=cursor.fetchone()
    conn.commit()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} Not found") 
    return Response(status_code=status.HTTP_204_NO_CONTENT) #Delete Request Returns Nothing

@app.put("/post/{id}")
def update_post(id:int,post:Post):
    
    cursor.execute(""" UPDATE posts SET title = %s,content = %s,published = %s WHERE id=%s RETURNING *""", 
                   (post.title,post.content,post.published,id))
    updated_post=cursor.fetchone()
    conn.commit()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} Not found")
    
    return {"Success:" f"Post {id} updated successfuly"" Updated Post: " f"{updated_post}"}
    
