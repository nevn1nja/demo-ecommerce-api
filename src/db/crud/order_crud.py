from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.api.models.order import OrderRequest
from src.db.crud.product_crud import get_product_by_id
from src.db.models.database_models import Order, OrderItem, OrderStatus
from src.utils.exception_handlers import InsufficientStockException, OrderCreationException
from src.utils.logger import logger


def create_order(db: Session, order_data: OrderRequest) -> Order:
    try:
        total_price = 0.0
        for item in order_data.items:
            product = get_product_by_id(db, item.product_id)
            logger.info(f"Product ID: {product.id}, Stock: {product.stock}, Price: {product.price}, Item: {item}")

            if not product or product.stock < item.quantity:
                raise InsufficientStockException(f"Insufficient stock for product ID {item.product_id}")
            total_price += product.price * item.quantity

        new_order = Order(total_price=total_price, status=OrderStatus.PENDING)
        db.add(new_order)
        db.flush()

        for item in order_data.items:
            new_item = OrderItem(order_id=new_order.id, product_id=item.product_id, quantity=item.quantity, )
            db.add(new_item)

            product = get_product_by_id(db, item.product_id)
            product.stock -= item.quantity

        db.commit()
        db.refresh(new_order)
        return new_order

    except InsufficientStockException as e:
        db.rollback()
        raise e
    except IntegrityError as e:
        db.rollback()
        raise OrderCreationException(f"Error creating order: {str(e)}")
    except Exception as e:
        db.rollback()
        raise OrderCreationException(f"Unexpected error: {str(e)}")
