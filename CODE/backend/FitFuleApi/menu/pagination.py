from rest_framework.pagination import LimitOffsetPagination


class RecipePagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100
