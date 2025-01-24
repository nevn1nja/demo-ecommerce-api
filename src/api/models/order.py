from typing import List

from pydantic import BaseModel, Field, ConfigDict, model_validator

from src.db.models.database_models import OrderStatus
from src.utils.exception_handlers import EmptyItemsException


class OrderId(BaseModel):
    id: int = Field(..., description="Unique identifier for the order")


class OrderItem(BaseModel):
    product_id: int = Field(..., description="ID of the product being ordered")
    quantity: int = Field(..., description="Quantity of the product being ordered")


class Order(OrderId):
    model_config = ConfigDict(from_attributes=True, extra='allow')
    items: List[OrderItem] = Field(..., description="List of products in the order")
    total_price: float = Field(..., description="Total price of the order")
    status: OrderStatus = Field(..., description="Status of the order")


class OrderRequest(BaseModel):
    items: List[OrderItem] = Field(..., description="List of products in the order")

    @model_validator(mode='before')
    @classmethod
    def check_items_not_empty(cls, values):
        items = values.get('items')
        if not items:
            raise EmptyItemsException('Order must contain at least one item.')
        return values
