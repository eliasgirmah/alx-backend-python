from django.urls import path
from . import views
# listings/urls.py


from .views import debug_user_view  # ✅ import this correctly

app_name = 'listings'

urlpatterns = [
    path('', views.listing_list, name='listing_list'),
    path('<int:pk>/', views.listing_detail, name='listing_detail'),
     path('logs/', views.view_logs, name='view_logs'),
     path('debug-user/', debug_user_view),

]
