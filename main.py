from datetime import datetime
from uuid import uuid4

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import OperationalError
from starlette.responses import JSONResponse

from src.api.routes.orders import orders_router
from src.api.routes.products import products_router
from src.utils.exception_handlers import InsufficientStockException, ProductIdException, EmptyItemsException, \
    InvalidOrderQuantityException
from src.utils.logger import logger

logger.info("Initializing fastapi application...")
app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors = exc.errors()
    error_details = [{"field": ".".join(map(str, error.get("loc", []))), "message": error.get("msg", "Invalid input")}
                     for error in errors]
    content = {"detail": "Validation error", "errors": error_details,
               "request": {"method": request.method, "url": str(request.url)}, }
    logger.info(f"Handling validation error: {content}")
    return JSONResponse(status_code=422, content=content, )


@app.exception_handler(InsufficientStockException)
async def insufficient_stock_exception_handler(request, exc: InsufficientStockException):
    return JSONResponse(status_code=422, content={"detail": str(exc)}, )


@app.exception_handler(ProductIdException)
async def insufficient_stock_exception_handler(request, exc: ProductIdException):
    return JSONResponse(status_code=422, content={"detail": str(exc)}, )

@app.exception_handler(EmptyItemsException)
async def empty_order_items_exception_handler(request, exc: EmptyItemsException):
    return JSONResponse(status_code=422, content={"detail": str(exc)}, )

@app.exception_handler(InvalidOrderQuantityException)
async def invalid_quantity_exception_handler(request, exc: InvalidOrderQuantityException):
    return JSONResponse(status_code=422, content={"detail": str(exc)}, )


@app.exception_handler(OperationalError)
async def database_outage_exception_handler(request, exc: OperationalError):
    error_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error_uuid = uuid4()
    """
    The team must be notified about the incident ASAP as this is a critical failure with potential system wide impact.
    """
    return JSONResponse(status_code=500,
        content={"detail": "We are currently experiencing technical difficulties, and our team has been notified. "
                           "Please try again later. We apologize for the inconvenience.", "timestamp": error_time,
            "error_id": str(error_uuid),
            "suggestion": "If the issue persists, please contact support with the error details."})


app.include_router(products_router)
app.include_router(orders_router)

logger.info("Fastapi application initialization successful...")
if __name__ == "__main__":
    uvicorn.run(app)
