from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session

from src.api.models.pagination_metadata import generate_pagination_metadata
from src.api.models.product import Product, Products, ProductRequest
from src.db.base import get_db
from src.db.crud.product_crud import get_products, create_product
from src.utils.logger import logger

logger.info("Initializing products router...")
products_router = APIRouter()


def validate_pagination_params(skip: int, limit: int):
    if skip < 0:
        raise HTTPException(status_code=422, detail="Skip parameter must be greater than or equal to 0.")
    if limit <= 0 or limit > 1000:
        raise HTTPException(status_code=422, detail="Limit must be between 1 and 1000.")


@products_router.get("/products/", response_model=Products)
def read_products(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    validate_pagination_params(skip, limit)
    products = get_products(db, skip=skip, limit=limit)
    pagination_data = generate_pagination_metadata(skip, limit, len(products), base_url=str(request.url).split("?")[0])

    return Products(data=products, meta=pagination_data)


@products_router.post("/products/", response_model=Product)
def create_new_product(product: ProductRequest, response: Response, db: Session = Depends(get_db)):
    response.status_code = 201
    return create_product(db, name=product.name, description=product.description, price=product.price,
                          stock=product.stock)


logger.info("Products router initialization successful...")
