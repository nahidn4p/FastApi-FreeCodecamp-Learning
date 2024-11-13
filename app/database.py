# import psycopg2
# import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL= 'postgresql://Nahid.Hasan:postgres@localhost:5432/fastapi'
engine=create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()    

# while True:
#     try:
#         conn=psycopg2.connect(host='localhost',dbname='fastapi',user="Nahid.Hasan",password="postgres",
#                              cursor_factory=psycopg2.extras.RealDictCursor)
#         cursor=conn.cursor()
#         print("Database Connection Successfull!")
#         break
#     except Exception as error:
#         print("Connection Unsuccessfull")
#         print("Error:",error)
#         time.sleep(2)


