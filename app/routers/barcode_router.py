from ..dependencies.utils import get_json_response
from ..config import settings
from ..schemas.barcode_details import BarcodeDetails
from fastapi import APIRouter
from typing import Any
from ..dependencies.constants import SYSTEM_PROMPT
from loguru import logger

barcode_router = APIRouter(
  prefix='/barcode',
  tags=['Fetch Details From Barcode']
)

# @barcode_router.get("/details", response_model=BarcodeDetails)
@barcode_router.get("/details")
async def api_barcode_details(barcode: int) -> dict:
  openfoodfacts_product_url = f'{settings.OPENFOODFACTS_API_URL}/product/{barcode}'
  response = await get_json_response(openfoodfacts_product_url)
  SYSTEM_PROMPT.format(data=response)
  logger.info(f"Updated SYSTEM_PROMPT: {SYSTEM_PROMPT}")
  return response
