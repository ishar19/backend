from .routers import barcode_router
from fastapi import FastAPI
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)

#Fast API App Instance
app = FastAPI()
app.include_router(barcode_router)

@app.get("/")
async def root():
    return {"message": "Hello Green Cart User!"}