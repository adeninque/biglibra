from django.shortcuts import render
from django.views.generic import ListView

from .models import (Book)

# Create your views here.
class BookListView(ListView):
  model = Book
  paginate_by = 10
  context_object_name = 'books'