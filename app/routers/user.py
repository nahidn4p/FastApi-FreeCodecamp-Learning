from .. import models,schemas,utils
from fastapi import APIRouter,Depends,status,HTTPException
from ..database import  get_db
from sqlalchemy.orm import Session


router=APIRouter(
    prefix="/user",
    tags=["user"]
)

@router.post("/createuser",status_code=status.HTTP_201_CREATED,response_model=schemas.User)
def create_user(user: schemas.UserBase,db: Session =  Depends(get_db)):
    #hash Password user.password

    hashed_password= utils.hashpass(user.password)
    user.password=hashed_password
    new_user=models.User(**user.dict()) #** for unpacking dictionary
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
     # Return the newly created post as a response
    return schemas.User.model_validate(new_user)  
@router.get("/{id}",response_model=schemas.User)
def get_user(id:int,db: Session =  Depends(get_db)):    
    user=db.query(models.User).filter(models.User.id==id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {id} Not found")
    return schemas.User.model_validate(user)    