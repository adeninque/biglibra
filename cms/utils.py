from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.models import Group


menu = [
  {'url': 'home', 'name': 'Home'},
  {'url': 'home', 'name': 'Home'},
  {'url': 'home', 'name': 'Home'},
]

class StuffReqiredMixin(LoginRequiredMixin, UserPassesTestMixin):
  login_url = reverse_lazy('home')
  
  def test_func(self) -> bool:
    return self.request.user.groups.filter(name = 'stuff').exists() or self.request.user.is_superuser
  
  def handle_no_permission(self) -> HttpResponseRedirect:
    return HttpResponseRedirect(self.login_url)


class MainMixin(StuffReqiredMixin):
  def get_custom_context(self, **kwargs):
    context = kwargs
    context.update({
      'menu': menu
    })
    return context