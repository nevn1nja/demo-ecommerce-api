from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from src.api.models.order import Order, OrderRequest
from src.db.base import get_db
from src.db.crud.order_crud import create_order
from src.utils.logger import logger

orders_router = APIRouter()


@orders_router.post("/orders/", response_model=Order)
async def create_new_order(order_create: OrderRequest, response: Response, db: Session = Depends(get_db)):
    logger.info(f"Creating new order with {len(order_create.items)} items")
    response.status_code = 201
    return create_order(db=db, order_data=order_create)
