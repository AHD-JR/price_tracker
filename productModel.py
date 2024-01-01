from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    absolute_name: str
    name: str
    description: Optional[str]
    price: str
    image: Optional[str]
    link: str
