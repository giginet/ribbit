from django import forms
from django.conf import settings
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, HttpResponseNotAllowed
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from models import User
from forms import RibbitUserChangeForm, RibbitUserCreationForm

class LoginView(FormView):

    class CustomAuthenticationForm(AuthenticationForm):
        username = forms.RegexField(
            label='Username',
            max_length=30,
            regex=r'^[\w-]+$',
            help_text = 'Required. 30 characters or fewer. Alphanumeric characters only (letters, digits, hyphens and underscores).',
            error_message = 'This value must contain only letters, numbers, hyphens and underscores.',
            widget=forms.TextInput(attrs={'class': 'username', 'placeholder': 'Username'})
        )
        password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'password', 'placeholder':'Password'}))

    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'

    def form_valid(self, form):
        redirect_to = settings.LOGIN_REDIRECT_URL
        auth_login(self.request, form.get_user())
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
        return HttpResponseRedirect(redirect_to)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    @method_decorator(sensitive_post_parameters('password'))
    def dispatch(self, request, *args, **kwargs):
        request.session.set_test_cookie()
        return super(LoginView, self).dispatch(request, *args, **kwargs)

class LogoutView(View):
    def post(self, request, *args, **kwargs):
        redirect_to = settings.LOGIN_URL
        auth_logout(request)
        return HttpResponseRedirect(redirect_to)

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed('')

class UserCreateView(CreateView):
    model = User
    form_class = RibbitUserCreationForm

class UserUpdateView(UpdateView):
    model = User
    form_class = RibbitUserChangeForm

    def get_object(self, queryset=None):
        return self.request.user

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserUpdateView, self).dispatch(request, *args, **kwargs)

class UserDetailView(DetailView):
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserDetailView, self).dispatch(request, *args, **kwargs)

class UserListView(ListView):
    model = User

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserListView, self).dispatch(request, *args, **kwargs)
