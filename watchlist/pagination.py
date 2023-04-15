from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'pageNumber'
    page_size_query_param = 'pageSize'
    