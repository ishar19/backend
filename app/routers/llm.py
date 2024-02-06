from fastapi import APIRouter, Depends, HTTPException,WebSocket
import google.generativeai as genai
from ..config import settings
import json
import markdown2

# Model initialization
genai.configure(api_key=settings.GEMINI_KEY)
history = []
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=history)

llm_router = APIRouter(
    prefix='/llm',
    tags=['Gemini Model Chat']
)


def to_html(markdown_format):
    return (
        markdown2.markdown(markdown_format)
        .replace("\\", "")
        .replace("<h1>", "<h7>")
        .replace("</h1>", "</h7>")
        .replace("\\\\", "")
        .replace("```", "")
        .replace("python", "")
        .replace("\n","<br>")
        .replace('"',"")
        .replace("#","<b>")
    )
    

def removeEmpty(paragraph):
    lines = paragraph.split('\n')
    non_empty_lines = [line for line in lines if line.strip() != '']
    cleaned_paragraph = '\n'.join(non_empty_lines)
    return cleaned_paragraph

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
        
            
            


