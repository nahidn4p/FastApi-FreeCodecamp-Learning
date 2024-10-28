from sqlalchemy import TIMESTAMP, text
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean

# Create a declarative base class
Base = declarative_base()

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default=text('true'), nullable=False)  # Use 'true' for Boolean
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email=Column(String, nullable=False, unique=True )
    password=Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)