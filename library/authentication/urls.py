from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.user_redirect, name='user_redirect'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('<int:user_id>/', views.user_account, name='user_account'),
    path('all/', views.get_all_users, name='all_users'),
    path('all/<int:user_id>', views.get_user_full_info, name='specific_user')
]
