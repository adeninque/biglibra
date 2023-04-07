from django import forms

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
