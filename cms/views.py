import uuid

from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404, HttpRequest
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
        form.save_m2m()
        return redirect(self.success_url)


class BookDetail(BaseCMSMixin, DetailView):
    model = Book
    slug_field = 'slug'
    template_name = 'cms/book-detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_custom_context(
            title=context['book'].title
        ))
        return context


class BookEdit(BaseCMSMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'cms/book-add.html'
    context_object_name = 'book'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_custom_context(
            title=' '.join(['Edit', context['book'].title])
        ))
        return context

    def form_valid(self, form):
        instance: Book = form.save()
        return redirect(instance.cms_detail_url())


def delete_book(request: HttpRequest, slug: str):
    instance: Book | None = None

    try:
        instance = Book.objects.get(slug=slug)
    except ValueError:
        raise Http404

    # instance.delete()
    if request.user.is_superuser or request.user.is_staff:
        instance.delete()
    return redirect(reverse_lazy('cms_home'))
