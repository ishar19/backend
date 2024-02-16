from pydantic import BaseModel
from typing import Optional

class ChatRequestDetails(BaseModel):
  barcode: Optional[int]
  user_query: str
