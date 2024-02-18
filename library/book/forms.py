from django import forms
from .models import Book
from author.models import Author


class BookForm(forms.ModelForm):
    authors = forms.ModelMultipleChoiceField(
        queryset=Author.get_all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False,
    )

    class Meta:
        model = Book
        fields = {'name', 'description', 'count', 'authors'}

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
