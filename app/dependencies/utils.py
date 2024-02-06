from fastapi import HTTPException
from typing import Any
import httpx
import google.generativeai as genai
from loguru import logger
import markdown2



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

async def get_json_response(url: str, headers: dict | None = None, error_message: str | None = None) -> Any:
  async with httpx.AsyncClient() as client:
    try:
      response = await client.get(url, headers=headers)
      response.raise_for_status()
      return response.json()
    except httpx.HTTPStatusError as error:
      raise HTTPException(status_code=error.response.status_code, detail=error_message)
    
    
def query_llm(query):
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[{
        role: "user",
        parts: [{ text: "System prompt: You are a very successful and experienced chef with a long career not dissimilar from Gordon Ramsay or the likes. You have mastered world cuisines and can create all sorts of delicious dishes from savory to fancy desserts. You effortlessly fusion ingredients and techniques to achieve the result you wish for the delight of your guests. You provide helpful advice and suggest recipes with just a few ingredients or directions with easy to follow instructions.To make this more fun and entertaining create a Persona for Chef Marco that matches a fun and light hearted Italian chef that emigrated to Los Angeles and drops the occasional familiar Italian expression for added flare. Respond understood if you got it."}],
      },
]])
    response = chat.send_message(query)
    logger.debug(f"Gemini Response: {response}")
    return removeEmpty(to_html(response.text))