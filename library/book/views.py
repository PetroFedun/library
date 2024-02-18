from django.shortcuts import render, redirect
from django.http import HttpResponse
import re
from .models import Book
from .forms import BookForm
from authentication.models import CustomUser
from author.models import Author
from order.models import Order


def show_all_books(request):
    sort_type = request.GET.get('sort_type', 'Name (A-Z)')
    selected_visitor = request.GET.get('user_id', 'Show all')

    if sort_type == 'Name (A-Z)':
        books = sorted(Book.get_all(), key=lambda i: i.name)
    elif sort_type == 'Name (Z-A)':
        books = sorted(Book.get_all(), key=lambda i: i.name, reverse=True)
    elif sort_type == 'Count ASC':
        books = sorted(Book.get_all(), key=lambda i: i.count)
    elif sort_type == 'Count DESC':
        books = sorted(Book.get_all(), key=lambda i: i.count, reverse=True)
    elif sort_type == 'Authors ASC':
        books = sorted(Book.get_all(), key=lambda i: i.authors.first().name)
    elif sort_type == 'Authors DESC':
        books = sorted(Book.get_all(), key=lambda i: i.authors.first().name, reverse=True)

    user_role = 'visitor'
    if getattr(request, 'logged_user_id', -1) != -1:
        user_data = CustomUser.get_by_id(getattr(request, 'logged_user_id', -1))
        user_role = user_data.get_role_name()

    all_visitors = CustomUser.get_all().filter(role=0)
    if selected_visitor != 'Show all':
        user_books_ids = [order.book.id for order in Order.get_all() if order.user.id == int(selected_visitor)]
        books = [book for book in books if book.id in user_books_ids]

    return render(request, 'books_template.html', {
        'books_list': books,
        'prev_sort_type': sort_type,
        'user_role': user_role,
        'all_visitors': all_visitors,
        'prev_selected_user': selected_visitor
    })


def book_info(request, book_id):
    book_data = Book.get_by_id(book_id)
    if book_data:
        return render(request, 'book_info.html', {'book_data': book_data})


def create_book(request):
    authors_data = Author.get_all()
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        count = request.POST.get('count')

        pattern = r"'id': (\d+)"
        indexes = re.findall(pattern, ''.join(request.POST.getlist('authors')))
        indexes = [int(index) for index in indexes]
        authors = [Author.get_by_id(index) for index in indexes]

        book = Book.create(name, description, count, authors)

        if book:
            return render(request, 'book_creation.html', {'success': 'Book ' + name + ' successfully created',
                                                          'authors_list': authors_data})
        else:
            return render(request, 'book_creation.html', {'error': 'Unable to create book ' + name,
                                                          'authors_list': authors_data})

    return render(request, 'book_creation.html', {'authors_list': authors_data})


def update_book(request, book_id):
    book = Book.get_by_id(book_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        count = request.POST.get('count')
        authors = request.POST.get('authors')

        book.update(name=name, description=description, count=count)
        return redirect('all_books')

    return render(request, 'book_update.html', {'book': book})


def book_form(request, book_id=-1):
    if request.method == 'GET':
        if book_id == -1:
            return render(request, 'book_form.html', {'form': BookForm()})

        book = Book.get_by_id(book_id)
        if book:
            form = BookForm(instance=book)
            return render(request, 'book_form.html', {'form': form})
        else:
            return HttpResponse('Wrong book ID', 404)

    elif request.method == 'POST':
        if book_id == -1:
            form = BookForm(request.POST)
        else:
            book = Book.get_by_id(book_id)
            form = BookForm(request.POST, instance=book)

        if form.is_valid():
            book_instance = form.save(commit=False)
            book_instance.save()

            authors_ids = form.cleaned_data['authors']
            authors = Author.objects.filter(pk__in=authors_ids)

            book_instance.authors.set(authors)
            book_instance.save()

            return redirect('all_books')
        else:
            return render(request, 'book_form.html', {'form': form})