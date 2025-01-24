from typing import List

from pydantic import BaseModel, Field

from src.db.models.database_models import OrderStatus

class OrderId(BaseModel):
    id: int = Field(..., description="Unique identifier for the order")

class OrderItem(BaseModel):
    product_id: int = Field(..., description="ID of the product being ordered")
    quantity: int = Field(..., gt=0, description="Quantity of the product being ordered")

class Order(OrderId):
    items: List[OrderItem] = Field(..., description="List of products in the order")
    total_price: float = Field(..., description="Total price of the order")
    status: OrderStatus = Field(..., description="Status of the order")

class OrderRequest(BaseModel):
    items: List[OrderItem] = Field(..., description="List of products in the order")
