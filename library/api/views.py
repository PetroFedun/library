from django.shortcuts import render
from .serializers import *
from authentication.models import CustomUser
from order.models import Order
from author.models import Author
from rest_framework import generics


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

class AuthorCreateView(generics.CreateAPIView):
    serializer_class = AuthorSerializer


class AuthorListView(generics.ListAPIView):
    serializer_class = AuthorListSerializer
    queryset = Author.objects.all()

class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()


class UserOrders(generics.ListAPIView):
    serializer_class = UserOrdersListSerializer
    queryset = Order.objects.all()

class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
