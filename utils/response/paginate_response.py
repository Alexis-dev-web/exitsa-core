from django.core.paginator import Page


class PaginateResponse:
    
    def to_json(self, object: Page, total_pages: int, items: list = []) -> dict:
        return {
            'total_pages': total_pages,
            'next_page': object.has_next(),
            'previous': object.has_previous(),
            'items': items
        }
