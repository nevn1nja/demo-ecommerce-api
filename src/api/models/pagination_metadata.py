from typing import Optional

from pydantic import BaseModel


class PaginationMetadata(BaseModel):
    next_page: Optional[str]
    previous_page: Optional[str]


def generate_pagination_metadata(skip: int, limit: int, current_products_len: int, base_url: str):
    next_skip = skip + limit
    prev_skip = max(skip - limit, 0)
    next_page, previous_page = None, None

    if current_products_len == limit:
        next_page = f'{base_url}?skip={next_skip}&limit={limit}'

    if skip > 0:
        previous_page = f'{base_url}?skip={prev_skip}&limit={limit}'

    return PaginationMetadata(next_page=next_page, previous_page=previous_page)
