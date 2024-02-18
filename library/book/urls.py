from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.show_all_books, name='all_books'),
    path('<int:book_id>/', views.book_info, name='book_info'),
    path('creation/', views.book_form, name='book_creation'),
    path('update/<int:book_id>/', views.book_form, name='book_update')
]
