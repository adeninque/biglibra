from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, DeleteView, TemplateView
from django.urls import reverse_lazy
from libra.models import Book
# Create your views here.

menu = [
    {'url': 'app_home', 'name': 'About'}
]

class BookHome(ListView):
    model = Book
    template_name = 'app/home.html'
    context_object_name = 'books'
    extra_context = {'title': 'HOME'}


class BookDetail(DetailView):
    model = Book
    template_name = 'app/book.html'
    context_object_name = 'book'
