import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from src.api.routes.orders import orders_router
from src.api.routes.products import products_router
from src.utils.exception_handlers import InsufficientStockException
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


app.include_router(products_router)
app.include_router(orders_router)

logger.info("Fastapi application initialization successful...")
if __name__ == "__main__":
    uvicorn.run(app)
