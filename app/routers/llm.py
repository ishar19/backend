from fastapi import APIRouter, Depends, HTTPException,WebSocket
import google.generativeai as genai
from ..config import settings
from ..dependencies.utils import query_llm
import json
from ..crud import get_product
from loguru import logger

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

@llm_router.get("/chat")
async def chat_endpoint(user_query,barcode):
    barcode_details = get_product(barcode)
    logger.debug(f"Barcode details: {barcode_details}")
    response  = query_llm(user_query, barcode_details)
    return response
    
    
        
            
            


