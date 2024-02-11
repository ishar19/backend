from ..database import get_db
from fastapi import APIRouter
from loguru import logger
from typing import List, Dict
from fastapi import Depends, Query
from ..models import History
from sqlalchemy.orm import Session
from ..database import db
from sqlalchemy import desc
from ..schemas.history import HistoryResponse
from ..crud import fetch_history

history_router = APIRouter(
  prefix='/history',
  tags=['Fetch History']
)


@history_router.get("/fetch/{user_id}")
def get_history(user_id: int, db: Session = Depends(get_db)) -> List[dict]:
  return fetch_history(user_id, db)
