from django.urls import path

from .views import (Home,
                    AddBook,
                    BookDetail)


urlpatterns = [
    path('', Home.as_view(), name='cms_home'),
    path('add-book', AddBook.as_view(), name='cms_add_book'),
    path('book/<slug:slug>', BookDetail.as_view(), name='cms_book_detail'),
]