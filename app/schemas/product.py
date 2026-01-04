from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from decimal import Decimal


class ProductBase(BaseModel):
    name: str = Field(min_length=2, max_length=255, example="Punching Bag")
    price: Decimal = Field(gt=0, example=7599.99)
    stock: int = Field(ge=0, example=50)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass

