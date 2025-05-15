from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from config.database import engine, get_db
from app.models import user,property


from app.api.property_router import app as property_router

# 데이터베이스 테이블 생성
user.Base.metadata.create_all(bind=engine)
property.Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(property_router, tags=["property"])


@app.get("/")
def read_root():
    return {"Hello": "World"}

