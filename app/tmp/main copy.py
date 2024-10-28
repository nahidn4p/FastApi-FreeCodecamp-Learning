
import psycopg
import time
from typing import Optional
from fastapi import *
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from psycopg.rows import dict_row
while True:
    try:
        conn=psycopg.connect(host='localhost',dbname='fastapi',user="Nahid.Hasan",password="Post@123",
                             row_factory=dict_row)
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
    post_dict=post.dict()
    post_dict["id"]=randrange(0,100000)
    my_posts.append(post_dict)
    return {"data": my_posts}

@app.get("/post/{id}") 
def get_post(id:int):
    print(id)
    post=find_post(id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} Not found")
    return {"post_details": f"Here is your post {id}: {post}"}

@app.delete("/post/{id}",status_code=status.HTTP_204_NO_CONTENT)
def del_post(id:int):
    index=find_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} Not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT) #Delete Request Returns Nothing

@app.put("/post/{id}")
def update_post(id:int,post:Post):
    index=find_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} Not found")
    post_dict=post.dict()
    post_dict["id"]=id
    my_posts[index]=post_dict
    return {"Success:" f"Post {id} updated successfuly"" Updated Post: " f"{post_dict}"}
    
