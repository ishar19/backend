from ..dependencies.utils import get_json_response
from ..config import settings
from ..schemas.barcode_details import BarcodeDetails, RequestDetails
from fastapi import APIRouter, HTTPException
from typing import Any
from loguru import logger
from ..crud import create_new_product

history_router = APIRouter(
  prefix='/history',
  tags=['Fetch History']
)
