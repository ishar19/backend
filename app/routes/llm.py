from fastapi import APIRouter, Depends, HTTPException
import google.generativeai as genai

# Model initialization

history = []
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=history)

router = APIRouter()


