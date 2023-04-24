from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import redirect


# Create your views here.
class Login(LoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('home')

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return "/admin"
        elif user.is_staff:
            return reverse_lazy('cms_home')
        return super().get_success_url()


class ChangePass(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy("home")


def logout_view(request: HttpRequest):
    logout(request)
    return redirect(reverse_lazy('home'))

