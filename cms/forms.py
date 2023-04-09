from datetime import date

from django import forms
from django.core.validators import MinValueValidator, RegexValidator

from libra.models import (
    Book,
    Borrow,
    Authors,
    Categories
)


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'copies', 'cover', 'authors', 'cat')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'copies': forms.NumberInput(attrs={'class': 'form-control'}),
            'authors': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'cover': forms.FileInput(attrs={'style': 'height: 100%; display: inline-block;'}),
            'cat': forms.Select(attrs={'class': 'form-select'}),
        }


class BorrowForm(forms.ModelForm):
    date_regex = RegexValidator(
        regex=r'^\d{4}-\d{2}-\d{2}$',
        message='Date must be in yyyy-mm-dd format'
    )
    min_date = MinValueValidator(date.today())

    deadline = forms.DateField(widget=forms.DateInput(attrs={'value': date.today()}),
                               validators=[date_regex,
                                           min_date],
                               )

    class Meta:
        model = Borrow
        fields = ('deadline', 'status', 'borrower',)
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'borrower': forms.Select(attrs={'class': 'form-select'}),
        }
