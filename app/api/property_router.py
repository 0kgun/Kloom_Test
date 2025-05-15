from sqlalchemy.orm import Session


from fastapi import APIRouter

app = APIRouter(
    prefix="/property",
    tags=["property"]
)


@app.get("/test")
async def test_property():
    return {"message": "Property test"}


@app.get("/test2")
async def test_property2():
    return {"message": "Property test2"}

