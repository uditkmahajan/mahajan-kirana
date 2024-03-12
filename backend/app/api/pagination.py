from rest_framework.pagination import PageNumberPagination

class AppReviewPagination(PageNumberPagination): 
    page_size = 10
