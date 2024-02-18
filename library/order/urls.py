from django.urls import path
from .views import order_list, create_order, close_order

urlpatterns = [
    path('', order_list, name='order_list'),
    path('create/', create_order, name='create_order'),
    path('close/<int:order_id>/', close_order, name='close_order'),
]
