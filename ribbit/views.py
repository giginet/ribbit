from django.views.generic.base import RedirectView, TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse

from apps.rooms.models import Room

class LoginView(TemplateView):
    """
    View class for not authenticated users.
    """
    template_name = 'ribbit/login.html'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['login_form'] = AuthenticationForm(data=self.request.POST)
        return context

class LobbyView(TemplateView):
    """
    View class for autheticated users.
    """
    template_name = 'ribbit/lobby.html'

    def get_context_data(self, **kwargs):
        context = super(LobbyView, self).get_context_data(**kwargs)
        context['joined_rooms'] = Room.objects.get_joined_rooms(self.request.user)
        context['not_joined_rooms'] = Room.objects.get_not_joined_rooms(self.request.user)
        return context

class IndexView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return reverse("ribbit_lobby")
        return reverse("users_login")
