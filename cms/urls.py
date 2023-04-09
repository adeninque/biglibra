from django.urls import path

from .views import (Home,
                    AddBook,
                    BookDetail,
                    BookEdit,
                    delete_book,
                    AddBorrow)


urlpatterns = [
    path('', Home.as_view(), name='cms_home'),
    path('add-book', AddBook.as_view(), name='cms_add_book'),
    path('book/<slug:slug>', BookDetail.as_view(), name='cms_book_detail'),
    path('book/<slug:slug>/edit', BookEdit.as_view(), name='cms_book_edit'),
    path('book/<slug:slug>/delete', delete_book, name='cms_book_delete'),
    path('book/<slug:slug>/addborrow/', AddBorrow.as_view(), name='cms_add_borrow'),
]