from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr, Field



class User(BaseModel):
    id: int
    email: EmailStr 
    created_at: datetime

    class Config:
        from_attributes = True  # Enables extracting from attributes (e.g., ORM models)

# Base schema for shared fields
class PostBase(BaseModel):
    
    title: str
    content: str
    published: bool = True

    class Config:
        from_attributes = True  # Enables extracting from attributes (e.g., ORM models)

# Schema for post creation (request body)
class PostCreate(PostBase):
    pass  # No id or created_at needed in the request

# Full post schema (response body)
class Post(PostBase):
    id: int
    created_at: Optional[datetime] = None # Auto-generated by the database
    owner_id:int
    owner: User

    class Config:
        from_attributes = True  # Enables extracting from attributes (e.g., ORM models)


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email:EmailStr
    password: str        


class Token(BaseModel) :
    access_token: str
    token_type: str
class Tokendata(BaseModel):
    id : Optional[str] = None    


class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(strict=True, le=1)]
    class Config:
        from_attributes = True 

class PostOut(BaseModel):
    post: Post
    votes: int

    class Config:
        from_attributes = True  # Enables extracting from attributes (e.g., ORM models)
