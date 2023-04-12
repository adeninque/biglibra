from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, DeleteView, TemplateView
from django.urls import reverse_lazy
from libra.models import Book
# Create your views here.
from libra.views import BookListView

menu = [
    {'url': 'home', 'name': 'Home'}
]


class BookHome(ListView):
    model = Book
    template_name = 'app/home.html'
    context_object_name = 'books'
    extra_context = {'title': 'HOME'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'menu': menu})
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['books'] = context['books'].filter(title__icontains=search_input)
        context['search_input'] = search_input
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(BookHome, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-id")
        return qs


class BookDetail(DetailView):
    model = Book
    template_name = 'app/book.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'menu': menu})
        return context