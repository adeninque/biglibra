from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


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
        return self.success_url
