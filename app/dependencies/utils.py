from fastapi import HTTPException
from typing import Any
import httpx
import google.generativeai as genai
from loguru import logger
import markdown2
from ..schemas.barcode_details import BarcodeDetails


SYSTEM_PROMPT = f"""You are Eco-Friendly and Health Agent.
This is some data about a product in JSON Format. 
Try to answer questions with reference to this"""

def update_system_prompt(data):
  product = data.get('product')
  data = BarcodeDetails(
      id=product.get('id'),
      name=product.get('product_name'),
      image_url=product.get('image_url'),
      allergens=product.get('allergens'),
      brands=product.get('brands'),
      categories=product.get('categories'),
      countries=product.get('countries'),
      ecoscore_grade=product.get('ecoscore_grade'),
      ecoscore_score=product.get('ecoscore_score'),
      ingredients=product.get('ingredients_text_en'),
      nova_group=product.get('nova_group'),
      nutrient_levels=product.get('nutrient_levels') or {},
      nutriments=product.get('nutriments') or {},
      nutriscore_grade=product.get('nutriscore_grade'),
      nutriscore_score=product.get('nutriscore_score'),
      packaging=product.get('packaging_text_en'),
      warnings=product.get('ecoscore_extended_data').get('impact').get('warnings') or []
    )
  global SYSTEM_PROMPT
  SYSTEM_PROMPT = f"{SYSTEM_PROMPT}: data {data}"
  logger.debug(f"SYSTEM_PROMPT: {SYSTEM_PROMPT}")

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
      update_system_prompt(response.json())
      return response.json()
    except httpx.HTTPStatusError as error:
      raise HTTPException(status_code=error.response.status_code, detail=error_message)
    
    
def query_llm(query):
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])
    input = f'''
    SYSTEM_PROMPT:{SYSTEM_PROMPT} 
    user query: {query}
    '''
    logger.debug(f"Gemini Input: {input}")
    response = chat.send_message(input)
    logger.debug(f"Gemini Response: {response}")
    return removeEmpty(to_html(response.text))