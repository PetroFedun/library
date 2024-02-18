from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Order
from book.models import Book
from authentication.models import CustomUser


def order_list(request):
    today = timezone.now()
    user_id = getattr(request, 'logged_user_id', -1)
    user_role = getattr(request, 'logged_user_role', -1)
    user = CustomUser.get_by_id(user_id)
    if user_id != -1 and user_role == 1:
        orders = Order.get_all()
        orders.sort(key=lambda order: order.id)
        for order in orders:
            order.days_left = (order.plated_end_at - today).days
    elif user_id != -1 and user_role != 1:
        orders = Order.objects.filter(user=user_id)
        for order in orders:
            order.days_left = (order.plated_end_at - today).days
    else:
        login_message = "You are not logged in. Please log in to view the orders."
        login_link = "/user/login/"
        return render(request, 'order_list.html', {'login_message': login_message, 'login_link': login_link})
    return render(request, 'order_list.html', {'orders': orders, 'user': user})



def create_order(request):
    today = timezone.now().strftime("%Y-%m-%d")
    today_str = datetime.strptime(today, "%Y-%m-%d")

    max_day_str = today_str + timedelta(days=10)
    max_day = max_day_str.strftime("%Y-%m-%d")

    user_id = getattr(request, 'logged_user_id', -1)
    user = CustomUser.get_by_id(user_id)

    user.can_create_order = True
    not_returned_books = Order.get_not_returned_books()
    not_returned_user_ids = [order['user_id'] for order in not_returned_books]
    if user_id in not_returned_user_ids and user.role != 1:
        user.can_create_order = False

    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        user_id = request.POST.get('user_id') if request.POST.get('user_id') else user_id
        planned_end_at = request.POST.get('plated_end_at')

        book = Book.get_by_id(book_id)
        user = CustomUser.get_by_id(user_id)
        if book and user:
            order = Order.create(user=user, book=book, plated_end_at=planned_end_at)
            if order:
                return redirect('order_list')

    books = Book.get_all()
    not_returned_books = Order.get_not_returned_books()
    not_returned_book_ids = [order['book_id'] for order in not_returned_books]
    not_returned_user_book = [order['book_id'] for order in not_returned_books if order['user_id'] == user_id]
    if len(not_returned_user_book) > 0:
        user.not_returned_user_book = Book.get_by_id(not_returned_user_book[0])
    books = [book for book in books if book.count > not_returned_book_ids.count(book.id)]
    users = []
    if user.role == 1:
        not_returned_user_ids = [order['user_id'] for order in not_returned_books]
        users = CustomUser.get_all().exclude(role=1).exclude(id__in=not_returned_user_ids)
    return render(request, 'create_order.html', {'books': books, 'users': users, 'user': user, 'today': today, 'max_day': max_day})


def close_order(request, order_id):
    order = Order.get_by_id(order_id)
    book = Book.get_by_id(order.book_id)
    book_name = book.name
    visitor = CustomUser.get_by_id(order.user_id)
    visitor_name = visitor.first_name + " " + visitor.last_name

    if request.method == 'POST':
        confirm = request.POST.get('confirm')
        if confirm == 'yes':
            order.update(end_at=timezone.now())
            return redirect('order_list')

    return render(request, 'close_order.html', {'order': order, 'book': book_name, 'visitor': visitor_name})
