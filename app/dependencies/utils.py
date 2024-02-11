from fastapi import HTTPException
from typing import Any
import httpx
import google.generativeai as genai
from loguru import logger
import markdown2
from ..schemas.barcode_details import BarcodeDetails


SYSTEM_PROMPT = """You are Eco-Friendly and Health Agent.
This is some {data} about a product in JSON Format. 
Try to answer questions with reference to this"""

def get_prompt_data(data):
    logger.debug(f"Data: {data}")

    formatted_data = {
        "barcode": data.id,
        "name": data.name,
        "image_url": data.image_url,
        "allergens": data.allergens,
        "brands": data.brands,
        "categories": data.categories,
        "countries": data.countries,
        "ecoscore_grade": data.ecoscore_grade,
        "ecoscore_score": data.ecoscore_score,
        "ingredients": data.ingredients,
        "nova_group": data.nova_group,
        "nutrient_levels": data.nutrient_levels,
        "nutriments": data.nutriments,
        "nutriscore_grade": data.nutriscore_grade,
        "nutriscore_score": data.nutriscore_score,
        "packaging": data.packaging,
        "warnings": data.warnings
    }

    return formatted_data


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
  logger.debug(f"Fetching JSON from {url}")
  async with httpx.AsyncClient() as client:
    try:
      response = await client.get(url, headers=headers)
      response.raise_for_status()
      return response.json()
    except httpx.HTTPStatusError as error:
      raise HTTPException(status_code=error.response.status_code, detail=error_message)
    
    
def query_llm(query, data):
    data = get_prompt_data(data)
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])
    input = f'''
    SYSTEM_PROMPT:{SYSTEM_PROMPT.format(data=data)} 
    user query: {query}
    '''
    logger.debug(f"Gemini Input: {input}")
    response = chat.send_message(input)
    logger.debug(f"Gemini Response: {response}")
    return removeEmpty(to_html(response.text))