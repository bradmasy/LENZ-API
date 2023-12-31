from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnDict


class CustomLimitOffsetPagination(LimitOffsetPagination):
    limit_query_param = "limit"
    offset_query_param = "offset"
    offset = 0
    limit = 25
    count = 0

    def get_paginated_response(self, model, request, data):
        request_queries = request.query_params
        queries = ["title", "photo", "description", "active"]
        self.limit = int(request.query_params.get("limit", 25))
        self.offset = int(request.query_params.get("offset", 0))

        for i in queries:
            if i in request_queries.keys():
                self.count = len(data)
                break
            else:
                self.count = len(model.objects.all())
        self.request = request
        if isinstance(data, ReturnDict):  # if its a single entity
            self.count = len([data])

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
