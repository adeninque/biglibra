from django.urls import path

from .views import (
    Login,
    logout_view,
    ChangePass
)


urlpatterns = [
    path('login/', Login.as_view(), name='accounts_login'),
    path('logout/', logout_view, name='accounts_logout'),
    path('resetpass/', ChangePass.as_view(), name='accounts_reset')
    # path('recovery/')
]
