from .. import models,schemas,utils
from fastapi import *
from ..database import engine, get_db
from sqlalchemy.orm import Session
from typing import List, Optional

router=APIRouter(
    prefix="/post" ,#this will add /post for every app path
    tags=["post"]
)

@router.get("/test")
def root():
    return {"message": "Welcome"}

@router.get("/", response_model=List[schemas.PostCreate] )
def get_posts(db: Session =  Depends(get_db)):
    posts=db.query(models.Post).all()
    return [schemas.Post.model_validate(post) for post in posts]

@router.post("/createpost",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post: schemas.PostCreate,db: Session =  Depends(get_db)):
    

    new_post=models.Post(**post.dict()) #** for unpacking dictionary
    print(new_post)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
     # Return the newly created post as a response
    return schemas.Post.model_validate(new_post)  # Use Pydantic's model validate method

@router.get("/{id}") 
def get_post(id:int,db: Session =  Depends(get_db)):
    
    posts=db.query(models.Post).filter(models.Post.id==id).first()
    print(posts)
    if posts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} Not found")
    return {"Success": f"{posts}"}

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def del_post(id:int,db: Session =  Depends(get_db)):


    posts=db.query(models.Post).filter(models.Post.id==id)
    if posts.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} Not found") 
    posts.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT) #Delete Request Returns Nothing

@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int,post:schemas.PostCreate,db: Session =  Depends(get_db)):
    
    posts_query=posts=db.query(models.Post).filter(models.Post.id==id)
    posts=posts_query.first()

    if posts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} Not found")
    posts_query.update(post.dict())
    db.commit()
    return schemas.Post.model_validate(posts)
    #return {"Success:" f"Post {id} updated successfuly"}
