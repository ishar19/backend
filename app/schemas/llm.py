from pydantic import BaseModel

class ChatRequestDetails(BaseModel):
  barcode: int
  user_query: str
