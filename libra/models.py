from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
  title = models.CharField(max_length=255)
  slug = models.SlugField(unique=True)
  cover = models.ImageField(upload_to='cover/%y/%m/%d')
  copies = models.IntegerField()
  authors = models.ManyToManyField('Authors')
  
  def __str__(self): return self.title
  

class Borrow(models.Model):
  BORROWED = 'B'
  LOST = 'L'
  STATUS = [ 
    (BORROWED,'borrowed'),
    (LOST, 'lost'),
  ]
  when = models.DateField(auto_now_add=True)
  deadline = models.DateField()
  status = models.CharField(max_length=1, choices=STATUS, default=BORROWED)
  borrower = models.ForeignKey(User , on_delete=models.PROTECT)
  book = models.ForeignKey('Book', on_delete=models.CASCADE)
  
  def __str__(self): return ':'.join([self.borrower, self.book, self.deadline])
  

class Authors(models.Model):
  photo = models.ImageField('author_photos/%Y/%m/%d', default='defs/profile_default.svg')
  slug = models.SlugField(unique=True)
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)

  def get_full_name(self): return ' '.join([self.first_name, self.last_name])

  def __str__(self): return self.slug
  

class Categories(models.Model):
  name = models.CharField(max_length=255)
  slug = models.SlugField(unique=True)
  
  def __str__(self): return self.name