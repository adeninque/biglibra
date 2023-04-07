import uuid

from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy

from .utils import BaseCMSMixin
from libra.models import (
    Book,
)
from .forms import (
    BookForm,
)
from libra.views import (
    BookListView,
)


# Create your views here.
class Home(BaseCMSMixin, BookListView):
    template_name = 'cms/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_custom_context())
        return context

    def get_queryset(self):
        return self.model.objects.order_by('pk').reverse()


class AddBook(BaseCMSMixin, CreateView):
    model = Book
    template_name = 'cms/book-add.html'
    form_class = BookForm
    success_url = reverse_lazy('cms_home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_custom_context(
            title='CMS | ADD BOOK'
        ))
        return context

    def form_valid(self, form: BookForm) -> HttpResponse:
        instance: Book = form.save(commit=False)
        slug = instance.title.strip().lower().replace(' ', '-')

        if self.model.objects.filter(slug=slug).exists():
            slug = f'{slug}-{str(uuid.uuid4())[:8]}'

        instance.slug = slug
        instance.save()
        return redirect(self.success_url)
