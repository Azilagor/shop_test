from pydantic import BaseModel
from typing import Optional, List

class ProductCreate(BaseModel):
    name: str
    quantity: int
    price: float
    category_id: Optional[int] = None

class ProductOut(BaseModel):
    id: int
    name: str
    quantity: int
    price: float

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    client_id: int

class OrderOut(BaseModel):
    id: int
    client_id: int

    class Config:
        from_attributes = True

class AddItemRequest(BaseModel):
    order_id: int
    product_id: int
    quantity: int


class CategoryCreate(BaseModel):
    name: str
    parent_id: Optional[int] = None

class CategoryOut(BaseModel):
    id: int
    name: str
    parent_id: Optional[int] = None

    class Config:
        orm_mode = True
