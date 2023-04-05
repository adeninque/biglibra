from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy

from .utils import MainMixin
from libra.models import (
  Book,
)
from .forms import (
  BookForm,
)

# Create your views here.
class Home(MainMixin, TemplateView):
  template_name = 'cms/home.html'
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context.update(self.get_custom_context())
    return context
  

class AddBook(MainMixin, CreateView):
  model = Book
  template_name = 'cms/book-add.html'
  form_class = BookForm
  success_url = reverse_lazy('cms_home')
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context.update(self.get_custom_context(
      title = 'CMS | ADD BOOK'
    ))
    return context
  
  def form_valid(self, form: BookForm) -> HttpResponse:
    print(form.data)
    return redirect(self.success_url)