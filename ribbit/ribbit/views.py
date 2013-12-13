from django.views.generic.base import RedirectView, TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse

from rooms.models import Room

"""
View class for not authenticated users.
"""
class LoginView(TemplateView):
    template_name = 'ribbit/login.html'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['login_form'] = AuthenticationForm(data=self.request.POST)
        return context

"""
View class for autheticated users.
"""
class LobbyView(TemplateView):
    template_name = 'ribbit/lobby.html'

    def get_context_data(self, **kwargs):
        context = super(LobbyView, self).get_context_data(**kwargs)
        context['rooms'] = Room.objects.all()
        return context

class IndexView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return reverse("ribbit_lobby")
        return reverse("users_login")
