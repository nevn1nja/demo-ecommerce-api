from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.api.models.order import OrderRequest
from src.db.crud.product_crud import get_product_by_id
from src.db.models.database_models import Order, OrderItem, OrderStatus
from src.utils.exception_handlers import InsufficientStockException, OrderCreationException, ProductIdException, \
    InvalidOrderQuantityException
from src.utils.logger import logger


def create_order(db: Session, order_data: OrderRequest) -> Order:
    try:
        total_price = 0.0
        for item in order_data.items:
            if item.quantity <= 0:
                raise InvalidOrderQuantityException(f"Quantity must be greater than zero.")
            product = get_product_by_id(db, item.product_id)
            if product is None:
                raise ProductIdException(f"Product ID '{item.product_id}' not found.")

            logger.info(f"Product ID: {product.id}, Stock: {product.stock}, Price: {product.price}, Item: {item}")

            if not product or product.stock < item.quantity:
                raise InsufficientStockException(
                    f"Insufficient stock for product ID {item.product_id}, requested {item.quantity}, available {product.stock}.")
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

    except (InsufficientStockException, ProductIdException, InvalidOrderQuantityException) as e:
        db.rollback()
        raise e
    except IntegrityError as e:
        db.rollback()
        raise OrderCreationException(f"Error creating order: {str(e)}")
    except Exception as e:
        db.rollback()
        raise OrderCreationException(f"Unexpected error: {str(e)}")
