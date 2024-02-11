from ..database import get_db
from ..dependencies.utils import get_json_response
from ..config import settings
from ..crud import update_history, create_product_from_response, get_product
from ..schemas.barcode_details import BarcodeDetails, BarcodeLookupHistory, BarcodeRequestDetails
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any
from loguru import logger

barcode_router = APIRouter(
  prefix='/barcode',
  tags=['Fetch Details From Barcode']
)


@barcode_router.post("/details", response_model=BarcodeLookupHistory)
async def api_barcode_details(request:BarcodeRequestDetails, db: Session = Depends(get_db)) -> Any:

  logger.debug(f"Request: {request}")
  history_id = update_history(request.user_id, request.barcode, db)
  product = get_product(request.barcode, db)

  if product is not None:
    return BarcodeLookupHistory.from_product_history_id(product, history_id)
  
  openfoodfacts_product_url = f'{settings.OPENFOODFACTS_API_URL}/product/{request.barcode}'
  response: dict = await get_json_response(openfoodfacts_product_url)
  
  if response.get('status') == 1:
    response_product = response.get('product')
    product = create_product_from_response(response_product, db)
    return BarcodeLookupHistory.from_product_history_id(product, history_id)
  else:
    raise HTTPException(status_code=404, detail='Barcode not found')
