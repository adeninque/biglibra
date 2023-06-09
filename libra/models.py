from datetime import date

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    cover = models.ImageField(upload_to='book-cover/%y/%m/%d')
    copies = models.IntegerField()
    authors = models.ManyToManyField('Authors')
    cat = models.ForeignKey('Categories', on_delete=models.PROTECT, default=None)

    def __str__(self): return self.title

    def get_slugged_url(self, url_name: str):
        return reverse(viewname=url_name, kwargs={'slug': self.slug})

    def get_copies(self):
        return self.copies - self.borrow_set.all().count()

    def cms_detail_url(self):
        return self.get_slugged_url(url_name='cms_book_detail')

    def get_edit_url(self):
        return self.get_slugged_url(url_name='cms_book_edit')

    def get_delete_url(self):
        return self.get_slugged_url(url_name='cms_book_delete')

    def get_add_borrow_url(self):
        return self.get_slugged_url(url_name='cms_add_borrow')


class Borrow(models.Model):
    BORROWED = 'B'
    LOST = 'L'
    STATUS = [
        (BORROWED, 'borrowed'),
        (LOST, 'lost'),
    ]
    when = models.DateField(auto_now_add=True)
    deadline = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS, default=BORROWED)
    borrower = models.ForeignKey(User, on_delete=models.PROTECT)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)

    def __str__(self):
        return ' - '.join([self.borrower.__str__(),
                           self.book.__str__(),
                           self.deadline.strftime("%Y-%m-%d")])

    def get_pk_url(self, url_name: str):
        return reverse(viewname=url_name, kwargs={'pk': self.pk})

    def cms_detail_url(self):
        return self.get_pk_url(url_name='cms_borrow_detail')

    def get_edit_url(self):
        return self.get_pk_url(url_name='cms_edit_borrow')

    def get_return_url(self):
        return self.get_pk_url(url_name='cms_edit_return')

    def get_delta_time(self):
        today = date.today()
        delta = self.deadline - today
        if delta.days > 0:
            return {'label': 'Remaining', 'delta': f'{delta.days} days'}
        elif delta.days == 0:
            return {'label': 'Return day', 'delta': 'today'}
        return {'label': 'Overdue', 'delta': f'{abs(delta.days)} days'}


class Authors(models.Model):
    photo = models.ImageField('author_photos/%Y/%m/%d', default='defs/profile_default.svg')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def get_full_name(self): return ' '.join([self.first_name, self.last_name])

    def __str__(self): return self.get_full_name()


class Categories(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self): return self.name
