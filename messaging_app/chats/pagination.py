# chats/pagination.py

from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    page_size = 20  # 20 messages per page
    page_size_query_param = 'page_size'  # optional: client can override page size via ?page_size=
    max_page_size = 100  # max limit for page_size
