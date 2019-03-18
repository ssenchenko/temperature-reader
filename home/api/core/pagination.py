from rest_framework import pagination
from rest_framework import response


class SimplifiedPagination(pagination.PageNumberPagination):

    def get_paginated_response(self, data):
        return response.Response(data)
