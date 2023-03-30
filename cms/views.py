from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .utils import MainMixin

# Create your views here.
class Home(MainMixin, TemplateView):
  template_name = 'cms/home.html'
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context.update(self.get_custom_context())
    return context