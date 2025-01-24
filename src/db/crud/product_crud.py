from typing import cast

from sqlalchemy.orm import Session

from src.db.models.database_models import Product


def create_product(db: Session, name: str, description: str, price: float, stock: int):
    db_product = Product(name=name, description=description, price=price, stock=stock)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).order_by(Product.id).offset(skip).limit(limit).all()


def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(cast("ColumnElement[bool]", Product.id == product_id)).first()
