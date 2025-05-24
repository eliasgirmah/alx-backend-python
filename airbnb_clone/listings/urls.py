from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    path('', views.listing_list, name='listing_list'),
    path('<int:pk>/', views.listing_detail, name='listing_detail'),
     path('logs/', views.view_logs, name='view_logs'),

]
