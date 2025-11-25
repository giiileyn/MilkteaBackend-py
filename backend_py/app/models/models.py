from pydantic import BaseModel
from typing import List, Optional

class Stat(BaseModel):
    orders: int
    users: int
    products: int
    topProducts: Optional[List[dict]] = []

class LowStockItem(BaseModel):
    name: str
    stock: int
