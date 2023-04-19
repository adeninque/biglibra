from django.urls import path
from .views import *

urlpatterns = [
    path('', BookHome.as_view(), name='home'),
    path('book/<slug:slug>/', BookDetail.as_view(), name='book'),
    path('profile/<slug:slug>', Profile.as_view(), name='profile')
]
