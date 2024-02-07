from ..dependencies.utils import get_json_response
from ..config import settings
from ..schemas.barcode_details import BarcodeDetails
from fastapi import APIRouter, HTTPException
from typing import Any
from loguru import logger

barcode_router = APIRouter(
  prefix='/barcode',
  tags=['Fetch Details From Barcode']
)


@barcode_router.get("/details", response_model=BarcodeDetails)
async def api_barcode_details(barcode: int) -> Any:
  openfoodfacts_product_url = f'{settings.OPENFOODFACTS_API_URL}/product/{barcode}'
  response: dict = await get_json_response(openfoodfacts_product_url)
  if response.get('status') == 1:
    product = response.get('product')
    return BarcodeDetails(
      id=barcode,
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
