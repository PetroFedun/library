from django import forms
from .models import CustomUserManager,CustomUser
from order.models import Order

ROLE_CHOICES = (
    (0, 'visitor'),
    (1, 'librarian'),
)

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    middle_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = CustomUserManager
        fields = ['first_name', 'middle_name', 'last_name', 'email', 'role', 'password']

class AccountEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'middle_name', 'last_name', 'email']

class UserInfoForm(forms.ModelForm):
    orders = forms.ModelMultipleChoiceField(queryset=Order.objects.all(), label='Orders')

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'orders']

class UserSearchForm(forms.Form):
    search_term = forms.CharField(max_length=100, label='Search Users')