from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, DeleteView, TemplateView

# Create your views here.
def home_page(request):
    return HttpResponse('Hello')


class Home(TemplateView):
    template_name = 'app/home.html'
