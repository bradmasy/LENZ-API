from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList


class CustomLimitOffsetPagination(LimitOffsetPagination):
    limit_query_param = 25
    offset_query_param = 0
    offset = 0
    limit = 25
    count = 0

    def get_paginated_response(self, data):
        if isinstance(data, ReturnDict):
            self.count = len([data])
        if isinstance(data, ReturnList):
            self.count = len(data)
        return Response(
            {
                "count": self.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )

    def paginate_queryset(self, queryset, request, view=None):
        self.count = self.get_count(queryset)
        return super().paginate_queryset(queryset, request, view)

    def get_count(self, queryset):
        return queryset.count()
