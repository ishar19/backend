from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from controller import llm_router

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
    return {"message": "Hello from green cart backend"}


app.include_router(llm_router, prefix="/v1", tags=["LLM Services"])