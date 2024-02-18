from django.urls import path
from .views import author_list, create_author, update_author, delete_author

urlpatterns = [
    path('', author_list, name='author_list'),
    path('create/', create_author, name='create_author'),
    path('update/<int:author_id>/', update_author, name='update_author'),
    path('delete/<int:author_id>/', delete_author, name='delete_author'),
]