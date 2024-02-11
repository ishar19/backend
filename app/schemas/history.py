from pydantic import BaseModel

class HistoryResponse(BaseModel):
    id: str
    barcode: str