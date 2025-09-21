
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination class for the API.

    Provides consistent pagination across all API endpoints with:
    - Default page size of 20 items
    - Maximum page size of 100 items
    - Customizable page size query parameter
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class SmallResultsSetPagination(PageNumberPagination):
    """
    Small pagination class for endpoints with smaller result sets.

    Provides pagination with:
    - Default page size of 10 items
    - Maximum page size of 50 items
    - Customizable page size query parameter
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class LargeResultsSetPagination(PageNumberPagination):
    """
    Large pagination class for endpoints with larger result sets.

    Provides pagination with:
    - Default page size of 50 items
    - Maximum page size of 200 items
    - Customizable page size query parameter
    """
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200
