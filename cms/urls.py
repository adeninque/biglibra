from django.urls import path

from .views import (Home,
                    AddBook,)


urlpatterns = [
  path('', Home.as_view(), name='cms_home'),
  path('add-book', AddBook.as_view(), name='cms_add_book'),
]