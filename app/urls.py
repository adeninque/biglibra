from django.urls import path
from .views import *

urlpatterns = [
    path('', BookHome.as_view(), name='home'),
    path('book/<slug:slug>/', BookDetail.as_view(), name='book'),
    path('login/', Login.as_view(), name='login')
]
