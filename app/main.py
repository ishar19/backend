
from .routers import barcode_router,llm_router
from fastapi import FastAPI
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI



#Fast API App Instance
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

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


@app.get("/")
async def root():
    return {"message": "Hello from green cart backend"}


app.include_router(llm_router)
app.include_router(barcode_router)

