from django.db.models import QuerySet
from ninja import Field, Schema
from ninja.pagination import PaginationBase


class CustomPagination(PaginationBase):
    """
    自定义分页器
    """

    class Input(Schema):
        page: int = Field(1, gt=0)
        size: int = 6

    class Output(Schema):
        success: bool = True
        code: dict = {"code": "", "msg": ""}
        total: int
        page: int
        size: int

    def paginate_queryset(self, queryset: QuerySet, pagination: Input, **params):
        page: int = pagination.page
        size: int = pagination.size
        offset = (page - 1) * size
        data = {
            "items": queryset[offset: offset + size],
            "total": len(queryset),
            "page": page,
            "size": size
        }
        return data
