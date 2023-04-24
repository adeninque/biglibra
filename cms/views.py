import uuid

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.http import HttpResponse, Http404, HttpRequest
from django.urls import reverse_lazy

from .utils import BaseCMSMixin
from libra.models import (Book,
                          Borrow)
from .forms import (BookForm,
                    BorrowForm,
                    CustomerCreationForm)

from libra.views import (BookListView)


# Create your views here.
class Home(BaseCMSMixin, BookListView):
    template_name = 'cms/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_custom_context())
        return context


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
            title=context['book'].title,
            borrows=context['book'].borrow_set.exclude(status='L').order_by('deadline'),
            lost_borrows=context['book'].borrow_set.filter(status='L')
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

    if request.user.is_superuser or request.user.is_staff:
        instance.delete()
    return redirect(reverse_lazy('cms_home'))


class AddBorrow(BaseCMSMixin, CreateView):
    model = Borrow
    template_name = 'cms/borrow-form.html'
    form_class = BorrowForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_custom_context(
            title='CMS | ADD BORROW'
        ))
        return context

    def form_valid(self, form):
        book_slug: str | None = self.kwargs.get('slug', None)
        book_instance: Book | None = None
        borrow_instance: Borrow = form.save(commit=False)

        if not book_slug:
            raise Http404

        try:
            book_instance = Book.objects.get(slug=book_slug)
        except ValueError:
            raise Http404

        borrow_instance.book = book_instance
        borrow_instance.save()

        return redirect(book_instance.cms_detail_url())


class BorrowDetail(BaseCMSMixin, DetailView):
    model = Borrow
    pk_url_kwarg = 'pk'
    template_name = 'cms/borrow-detail.html'
    context_object_name = 'borrow'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context['borrow'].STATUS)
        context.update(self.get_custom_context(
            title=context['borrow'].__str__(),
        ))
        return context


class BorrowEdit(BaseCMSMixin, UpdateView):
    model = Borrow
    pk_url_kwarg = 'pk'
    template_name = 'cms/borrow-form.html'
    form_class = BorrowForm
    context_object_name = 'borrow'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_custom_context(
            title=f'EDIT | {context["borrow"].__str__()}'
        ))
        return context

    def form_valid(self, form):
        instance: Borrow = form.save(commit=True)
        return redirect(instance.cms_detail_url())


def return_book(request: HttpRequest, pk):
    instance: Borrow | None = None

    try:
        instance = Borrow.objects.get(pk=pk)
    except ValueError:
        raise Http404

    if request.user.is_superuser or request.user.is_staff:
        instance.delete()

    return redirect(instance.book.cms_detail_url())


class CustomersList(BaseCMSMixin, ListView):
    model = User
    template_name = 'cms/customers-list.html'
    context_object_name = 'users'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context.update(self.get_custom_context(
            title='Customers'
        ))

        return context

    def get_queryset(self):
        return User.objects.exclude(is_staff=True)


class CustomerCreate(BaseCMSMixin, CreateView):
    form_class = CustomerCreationForm
    template_name = 'cms/customer-create.html'
    success_url = reverse_lazy('cms_customers_list')

    def form_valid(self, form):
        password = User.objects.make_random_password()
        customer: User = form.save(commit=False)
        customer.password = make_password(password)
        customer.save()
        
        template = render_to_string('cms/email/temporary-password.html', {'user': customer,
                                                                          'password': password})
        msg = EmailMultiAlternatives(subject='[BigLibra] Registration',
                                     body=template,
                                     from_email='noreplay@noreplay.com',
                                     to=[customer.email])
        msg.attach_alternative(template, 'text/html')
        msg.send()

        return redirect(self.success_url)
