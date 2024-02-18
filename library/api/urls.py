from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('authors', AuthorListView)

urlpatterns = [
    path('user/', UserCreateView.as_view()),
    path('user/<int:user_id>/', UserDetailView.as_view()),
    path('user/<int:user_id>/order/', UserOrders.as_view()),
    path('user/<int:user_id>/order/<int:order_id>', UserOrders.as_view()),
    path('author/', AuthorCreateView.as_view()),
    path('author/<int:pk>/', AuthorDetailView.as_view()),
    path('order/', OrderCreateView.as_view()),
    path('order/<int:pk>/', OrderDetailView.as_view()),
    path('book/<int:pk>/', BookDetailView.as_view()),
    
]
