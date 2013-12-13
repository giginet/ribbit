from django.views.generic.base import View, TemplateView

"""
View class for not authenticated users.
"""
class LoginView(TemplateView):
    template_name = 'ribbit/login.html'

"""
View class for autheticated users.
"""
class LobbyView(TemplateView):
    template_name = 'ribbit/lobby.html'

class IndexView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            self.template_name = LobbyView.template_name
        else:
            self.template_name = LoginView.template_name
        return super(IndexView, self).get(request, *args, **kwargs)
