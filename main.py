from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from config.database import engine, get_db
from app.models import user,property

# 데이터베이스 테이블 생성
user.Base.metadata.create_all(bind=engine)
property.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# 데이터베이스 연결 테스트
@app.get("/db-test")
def test_db(db: Session = Depends(get_db)):
    try:
        # 데이터베이스 쿼리 실행 테스트
        db.execute('SELECT 1')
        return {"message": "Database connection successful!"}
    except Exception as e:
        return {"error": f"Database connection failed: {str(e)}"}
