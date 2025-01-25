from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict

from src.api.models.pagination_metadata import PaginationMetadata


class ProductId(BaseModel):
    id: int = Field(..., description="Unique identifier for the product")


class ProductRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="The name of the product")
    description: str = Field(..., min_length=1, max_length=1000, description="A brief description of the product")
    price: float = Field(..., gt=0, description="The price of the product, must be greater than 0")
    stock: int = Field(..., ge=0, description="The stock quantity, must be zero or a positive integer")


class Product(ProductRequest, ProductId):
    model_config = ConfigDict(from_attributes=True, extra='ignore')
    created_at: datetime = Field(..., description="Timestamp denoting when the product was created")
    updated_at: Optional[datetime] = Field(..., description="Timestamp denoting when the product was last updated")


class Products(BaseModel):
    data: List[Product]
    meta: PaginationMetadata
