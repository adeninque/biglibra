from django.urls import path
from .views import *

urlpatterns = [
    path('', BookHome.as_view(), name='home'),
    path('book/<slug:slug>/', BookDetail.as_view(), name='book'),
    path(r'profile/(?P<slug>[-\w.]+)/$', Profile.as_view(), name='profile')
]
