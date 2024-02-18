from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from .models import CustomUser, ROLE_CHOICES
from order.models import Order
from .forms import *

logged_user_id = -1


# def get_user_full_info(request, user_id):
#     today = timezone.now()
#     test_user_id = getattr(request, 'logged_user_id', -1)
#     user_role = getattr(request, 'logged_user_role', -1)
#     if test_user_id != -1 and user_role == 1:
#         user = CustomUser.get_by_id(user_id)
#         orders = Order.objects.filter(user=user_id)
#         for order in orders:
#             order.days_left = (order.plated_end_at - today).days
#     else:
#         login_message = "You are not logged in. Please log in to view the specific user."
#         login_link = "/user/login/"
#         return render(request, 'user_info.html', {'login_message': login_message, 'login_link': login_link})
#     return render(request, 'user_info.html', {'orders': orders, 'user_data': user})

def get_user_full_info(request, user_id):
    user = CustomUser.get_by_id(user_id=user_id)
    if request.method == 'POST':
        form = UserInfoForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            return render(request, 'user_info.html', {'user_data': user})
    else:
        form = UserInfoForm(instance=user)
    return render(request, 'user_info.html', {'form': form})


def get_all_users(request):
    if request.method == 'POST':
        form = UserSearchForm(request.POST)
        if form.is_valid():
            search_term = form.cleaned_data['search_term']
            users_list = CustomUser.get_all().filter(
                username__icontains=search_term, role=0
            )
    else:
        form = UserSearchForm()
        users_list = CustomUser.get_all().filter(role=0)

    return render(request, 'users_list.html', {'form': form, 'users_list': users_list})


def get_logged_user_id(request):
    return logged_user_id


def user_redirect(request):
    if logged_user_id == -1:
        return redirect('login')
    return redirect('user_account', logged_user_id)


def user_account(request, user_id):
    if logged_user_id == user_id:
        user_data = CustomUser.get_by_id(user_id)
        user_role = user_data.get_role_name()
        if request.method == 'POST':
            form = AccountEditForm(request.POST, instance=user_data)
            if form.is_valid():
                form.save()
                return redirect('user_account', user_id)
        else:
            form = AccountEditForm(instance=user_data)

        return render(request, 'user_account.html', {'user_data': user_data, 'user_role': user_role, 'form': form})
    return HttpResponse('Failed entering account')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, email=email, password=password)

            if user:
                global logged_user_id
                logged_user_id = user.id
                return redirect('user_account', user.id)
            else:
                return HttpResponse('Login failed')
    else:
        form = LoginForm()

    return render(request, 'user_login.html', {'form': form})


def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():

            first_name = form.cleaned_data['first_name']
            middle_name = form.cleaned_data['middle_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            role = int(form.cleaned_data['role'])

            if role == 0:
                user = CustomUser.objects.create_user(email=email, password=password, first_name=first_name,
                                                      middle_name=middle_name, last_name=last_name, is_active=True)
            else:
                user = CustomUser.objects.create_superuser(email=email, password=password, first_name=first_name,
                                                           middle_name=middle_name, last_name=last_name)

            if user:
                user.role = role
                user.save()

                global logged_user_id
                logged_user_id = user.id
                return redirect('user_account', user.id)
            else:
                return HttpResponse('Registration failed')
    else:
        form = RegistrationForm()
    return render(request, 'user_register.html', {'form': form})


def user_logout(request):
    global logged_user_id
    logged_user_id = -1
    return redirect('user_redirect')
