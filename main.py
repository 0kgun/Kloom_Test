from fastapi import FastAPI
from app.api.router.property_router import app as property_router
from config.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Kloom API",
    description="Real Estate Platform API",
    version="1.0.0"
)

# Include routers
app.include_router(property.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Kloom API"}

