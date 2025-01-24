class InsufficientStockException(Exception):
    pass


class ProductIdException(Exception):
    pass


class ProductCreationException(Exception):
    pass


class OrderCreationException(Exception):
    pass


class EmptyItemsException(OrderCreationException):
    pass


class InvalidOrderQuantityException(OrderCreationException):
    pass
