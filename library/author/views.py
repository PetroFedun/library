from django.shortcuts import render, redirect, get_object_or_404
from .models import Author
from .forms import AuthorForm


def author_list(request):
    user_id = getattr(request, 'logged_user_id', -1)
    user_role = getattr(request, 'logged_user_role', -1)
    if user_id != -1 and user_role == 1:
        authors = Author.objects.all().order_by('id')
        is_empty = not authors  # Check if the authors list is empty
        return render(request, 'author_list.html', {'authors': authors, 'is_empty': is_empty})
    elif user_id != -1 and user_role != 1:
        login_message = "You don't have permission to view authors list."
        return render(request, 'author_list.html', {'login_message': login_message})
    else:
        login_message = "You are not logged in. Please log in to view the authors."
        login_link = "/user/login/"
        return render(request, 'author_list.html', {'login_message': login_message, 'login_link': login_link})

def create_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('author_list')
    else:
        form = AuthorForm()

    return render(request, 'create_author.html', {'form': form})


def update_author(request, author_id):
    author = Author.get_by_id(author_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        patronymic = request.POST.get('patronymic')

        author.update(name=name, surname=surname, patronymic=patronymic)
        return redirect('author_list')

    return render(request, 'update_author.html', {'author': author})

def delete_author(request, author_id):
    author = Author.get_by_id(author_id)

    if request.method == 'POST':
        confirm = request.POST.get('confirm')
        if confirm == 'yes' and author and not author.books.exists():
            Author.delete_by_id(author_id)
            return redirect('author_list')

    return render(request, 'delete_author.html', {'author': author})
