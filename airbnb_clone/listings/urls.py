from django.urls import path
from .views import (
    listing_list,
    listing_detail,
    view_logs,
    debug_user_view,
    debug_all_users_view,
    debug_update_email_view,
    debug_fetch_users,
)

app_name = 'listings'

urlpatterns = [
    path('', listing_list, name='listing_list'),
    path('<int:pk>/', listing_detail, name='listing_detail'),
    path('logs/', view_logs, name='view_logs'),
    path('debug-user/', debug_user_view, name='debug_user'),
    path('debug-users/', debug_all_users_view, name='debug_all_users'),
    path('debug-update-email/', debug_update_email_view, name='debug_update_email'),
    path('debug-fetch-users/', debug_fetch_users, name='debug_fetch_users'),
]
