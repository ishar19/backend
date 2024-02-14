from ..database import get_db
from fastapi import APIRouter, Depends, HTTPException,WebSocket
import google.generativeai as genai
from ..config import settings
from ..dependencies.utils import query_llm
from ..schemas.llm import ChatRequestDetails
import json
from ..crud import get_product
from loguru import logger
from sqlalchemy.orm import Session

# Model initialization
genai.configure(api_key=settings.GEMINI_KEY)
history = []
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=history)

llm_router = APIRouter(
    prefix='/llm',
    tags=['Gemini Model Chat']
)


@llm_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    while True:
        message = await websocket.receive()
        
        if isinstance(message,bytes):
            data = json.loads(message.decode())
            message = data['text']
        else:
            if message == '!<FIN>!':
                await websocket.close()
                break
            response = chat.send_message([message], stream = True)
            
        for chunk in response:
            await websocket.send_text(chunk.text)
        await websocket.send_text('!<FIN>!')

@llm_router.post("/chat")
async def chat_endpoint(request: ChatRequestDetails, db: Session = Depends(get_db)) -> str:
    if request.barcode:
        product = get_product(request.barcode)
        logger.debug(f"Barcode details: {product.__dict__}")
    product = None    
    response  = query_llm(request.user_query, product)
    return response
    
    
        
            
            


