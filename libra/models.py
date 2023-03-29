from django.db import models

# Create your models here.
class Book(models.Model):
  title = models.CharField(max_length=255)
  slug = models.SlugField(unique=True)
  cover = models.ImageField(upload_to='cover/%y/%m/%d')
  authors = models.ManyToManyField('Authors')

class Borrow(models.Model):
  when = models.DateField(auto_now_add=True)
  deadline = models.DateField()
  book = models.ForeignKey('Authors', on_delete=models.PROTECT)

class Authors(models.Model):
  photo = models.ImageField('author_photos/%Y/%m/%d', default='defs/profile_default.svg')
  slug = models.SlugField(unique=True)
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)

class Categories(models.Model):
  name = models.CharField(max_length=255)
  slug = models.SlugField(unique=True)