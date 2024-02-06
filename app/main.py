
from .routers import barcode_router
from fastapi import FastAPI
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from controller import llm_router


#Fast API App Instance
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello Green Cart User!"}


origins = [
    "http://localhost",
    "http://localhost:3000",
]


@app.get("/")
async def root():
    return {"message": "Hello from green cart backend"}


app.include_router(llm_router, prefix="/v1", tags=["LLM Services"])
app.include_router(barcode_router)

