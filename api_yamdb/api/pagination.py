from rest_framework.pagination import PageNumberPagination

from core.constants import PAGE_SIZE


class CategoryPagination(PageNumberPagination):
    page_size = PAGE_SIZE
