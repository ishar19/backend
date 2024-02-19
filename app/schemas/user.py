from pydantic import BaseModel

class UserCreate(BaseModel):
    id : str
    name : str
    email : str
    image_url :str