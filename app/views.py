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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['books'] = context['books'].filter(title__icontains=search_input)
        context['search_input'] = search_input
        return context


class BookDetail(DetailView):
    model = Book
    template_name = 'app/book.html'
    context_object_name = 'book'


