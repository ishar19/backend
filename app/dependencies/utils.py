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
    response = model.generate_content(query)
    logger.debug(f"Gemini Response: {response}")
    return removeEmpty(to_html(response.text))