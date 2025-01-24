from enum import Enum as PyEnum

from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Enum, func, String
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    order_items = relationship('OrderItem', back_populates='product')

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, price={self.price}), stock={self.stock}>"


class OrderStatus(PyEnum):
    PENDING = "pending"
    COMPLETED = "completed"


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    total_price = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus, name="orderstatus"), nullable=False,
                    default=OrderStatus.PENDING)  # Storing as enum string
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    items = relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Order(id={self.id}, total_price={self.total_price}, status={self.status.value})>"


class OrderItem(Base):
    __tablename__ = 'order_items'

    order_id = Column(Integer, ForeignKey(Order.id, ondelete='CASCADE'), primary_key=True)
    product_id = Column(Integer, ForeignKey(Product.id, ondelete='CASCADE'), primary_key=True)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    order = relationship('Order', back_populates='items')
    product = relationship('Product', back_populates='order_items')

    def __repr__(self):
        return f"<OrderItem(order_id={self.order_id}, product_id={self.product_id}, quantity={self.quantity})>"
