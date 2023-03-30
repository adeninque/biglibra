from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .utils import MainMixin

# Create your views here.
class Home(MainMixin, TemplateView):
  template_name = 'cms/home.html'