from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    id : str
    name : str
    email : str
    image_url :Optional[str] = None