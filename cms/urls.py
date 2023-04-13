from django.urls import path

from .views import (Home,
                    AddBook,
                    BookDetail,
                    BookEdit,
                    delete_book,
                    BorrowDetail,
                    AddBorrow,
                    BorrowEdit,
                    return_book,
                    CustomersList)


urlpatterns = [
    path('', Home.as_view(), name='cms_home'),
    path('add-book/', AddBook.as_view(), name='cms_add_book'),
    path('book/<slug:slug>/', BookDetail.as_view(), name='cms_book_detail'),
    path('book/<slug:slug>/edit', BookEdit.as_view(), name='cms_book_edit'),
    path('book/<slug:slug>/delete', delete_book, name='cms_book_delete'),
    path('borrow/<int:pk>/', BorrowDetail.as_view(), name='cms_borrow_detail'),
    path('book/<slug:slug>/addborrow/', AddBorrow.as_view(), name='cms_add_borrow'),
    path('borrow/<int:pk>/edit/', BorrowEdit.as_view(), name='cms_edit_borrow'),
    path('borrow/<int:pk>/return/', return_book, name='cms_edit_return'),
    path('customers/', CustomersList.as_view(), name='cms_customers_list')
]