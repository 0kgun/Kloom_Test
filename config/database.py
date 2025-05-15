from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL 연결 설정
DATABASE_URL = "mysql+pymysql://root:726506@localhost:3306/kloomtest?charset=utf8"

# 데이터베이스 엔진 생성
engine = create_engine(
    DATABASE_URL,
    echo=True  # SQL 쿼리 로깅을 위한 설정
)

# 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모델 기본 클래스 생성
Base = declarative_base()

# 데이터베이스 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 