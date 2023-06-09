from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, DeleteView, TemplateView
from django.urls import reverse_lazy
from libra.models import Book
# Create your views here.
from libra.views import BookListView
from django.contrib.auth.models import User

menu = [

]


class BookHome(BookListView):
    template_name = 'app/home.html'
    extra_context = {'title': 'HOME'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'menu': menu})
        return context


class BookDetail(DetailView):
    model = Book
    template_name = 'app/book.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'menu': menu})
        return context


class Profile(DetailView):
    model = User
    template_name = 'app/profile.html'
    context_object_name = 'user'
    slug_field = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'menu': menu})
        return context

