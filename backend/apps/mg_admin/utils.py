from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


def jwt_response_payload_handler(token, user=None, request=None):
    """自定义jwt认证成功返回的数据"""
    return {
        'token': token,
        'id': user.id,
        'username': user.username,
    }


class PageNumPagination(PageNumberPagination):

    page_size_query_param = 'pagesize'
    max_page_size = 10

    def get_paginated_response(self, data):

        return Response({
            'count': self.page.paginator.count,
            'lists': data,
            'page': self.page.number,  # 页码数
            'pages': self.page.paginator.num_pages,  # 总页数
            'pagesize': self.max_page_size,  # 每页记录数
        })

