from . import PageNumberPagination
from rest_framework.response import Response

class PostsPaginator(PageNumberPagination):
    page_size = 2

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'first': self.get_first_link(),
                'last': self.get_last_link(),
                'pages': self.get_pages(),
            },
            'index': self.page.number,
            'count': self.page.paginator.count,
            'posts': data,
        })
