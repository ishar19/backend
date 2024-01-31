from fastapi import APIRouter, Depends, HTTPException,WebSocket
import google.generativeai as genai
import config
import json

# Model initialization
genai.configure(api_key=config.GEMINI_KEY)
history = []
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=history)

router = APIRouter()

@router.websocket("/ws")
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
        
            
            


