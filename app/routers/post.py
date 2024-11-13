from .. import models,schemas
from fastapi import APIRouter,Depends,status,HTTPException,Response
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import oauth2

router=APIRouter(
    prefix="/post" ,#this will add /post for every app path
    tags=["post"]
)

@router.get("/test")
def root():
    return {"message": "Welcome"}

@router.get("/own", response_model=List[schemas.Post] )
def get_posts(db: Session =  Depends(get_db),
                current_user :int = Depends(oauth2.get_current_user)):
    posts=db.query(models.Post).filter(models.Post.owner_id==current_user.id).all()
    #return [schemas.Post.model_validate(post) for post in posts]
    return posts


@router.get("/", response_model=List[schemas.Post] )
def get_posts(db: Session =  Depends(get_db),
                current_user :int = Depends(oauth2.get_current_user),
                limit: int =10,
                skip: int = 0,
                search: Optional[str]= ""
                ):
    posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return [schemas.Post.model_validate(post) for post in posts]

@router.post("/createpost",status_code=status.HTTP_201_CREATED,response_model=schemas.Post )
def create_post(post: schemas.PostCreate,db: Session =  Depends(get_db),
                current_user :int = Depends(oauth2.get_current_user)):
    
    #print(current_user)
    new_post=models.Post(owner_id=current_user.id,**post.model_dump()) #** for unpacking dictionary
    print(new_post)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
     # Return the newly created post as a response
    return schemas.Post.model_validate(new_post)  # Use Pydantic's model validate method

@router.get("/{id}",response_model=schemas.Post) 
def get_post(id:int,db: Session =  Depends(get_db),
            current_user :int = Depends(oauth2.get_current_user)):
    
    posts=db.query(models.Post).filter(models.Post.id==id).first()

    print(posts)
    if posts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} Not found")
    return posts

@router.delete("/{id}",response_model=schemas.Post)
def del_post(id:int,db: Session =  Depends(get_db),
                current_user :int = Depends(oauth2.get_current_user)):


    post = db.query(models.Post).filter(models.Post.id == id).first()

    # Check if post exists
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found")
    
    # Authorization check
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")
    
    # Delete post and commit changes
    db.query(models.Post).filter(models.Post.id == id).delete()
    db.commit()
    
    # Return 204 No Content
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int,post:schemas.PostCreate,db: Session =  Depends(get_db),
                current_user :int = Depends(oauth2.get_current_user)):
    
    posts_query=posts=db.query(models.Post).filter(models.Post.id==id)
    posts=posts_query.first()
    print(posts)

    if posts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} Not found")
    if posts.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not Authorized to perform this action")
    posts_query.update(post.model_dump())
    db.commit()
    return posts
    