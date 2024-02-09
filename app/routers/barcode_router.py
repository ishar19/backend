from ..dependencies.utils import get_json_response
from ..config import settings
from ..schemas.barcode_details import BarcodeDetails, RequestDetails
from fastapi import APIRouter, HTTPException
from typing import Any
from loguru import logger
from ..crud import create_new_product

barcode_router = APIRouter(
  prefix='/barcode',
  tags=['Fetch Details From Barcode']
)


@barcode_router.post("/details", response_model=BarcodeDetails)
async def api_barcode_details(request:RequestDetails) -> Any:
  logger.debug(f"Request: {request}")
  try:
      id = create_new_product(request.user_id, request.barcode)
  except:
    raise HTTPException(status_code=400, detail="Failed to create a new barcode. Integrity constraint violated.")
  
  openfoodfacts_product_url = f'{settings.OPENFOODFACTS_API_URL}/product/{request.barcode}'
  response: dict = await get_json_response(openfoodfacts_product_url)
  if response.get('status') == 1:
    product = response.get('product')
    return BarcodeDetails(
      history_id=id,  
      id=request.barcode,
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
      
  else:
    raise HTTPException(status_code=404, detail='Barcode not found')
