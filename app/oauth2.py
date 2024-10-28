from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import datetime, timedelta, timezone
from . import schemas,database,models
from sqlalchemy.orm import Session

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')
SECRET_KEY="ashbdy874bi4tbjwkdfyufg8ihfjknfjabfhasbfjlkfnm4e8932bfjlfnsldngjkdsb6813vfb2iyeb8yv"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc) +timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})


    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt



def verify_access_token(token: str,credentials_exception ):

    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id: str =str(payload.get("user_id"))
        if id is None:
            return credentials_exception
        token_data=schemas.Tokendata(id=id)
    except jwt.DecodeError:
        raise credentials_exception
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session= Depends(database.get_db)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                        detail="COULD NOT VALIDATE CREDENTIALS",
                                       headers={"WWW-authenticate" : {"Bearer"} }
                                       )
    token= verify_access_token(token,credentials_exception)
    user=db.query(models.User).filter(models.User.id==token.id),first()
    return user

