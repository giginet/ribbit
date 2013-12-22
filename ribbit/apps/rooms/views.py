from django import forms
from django.http.response import HttpResponseForbidden
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from ribbit.apps.users.models import User

from ribbit.apps.rooms.models import Room

class RoomCreateView(CreateView):
    """
    View class that to create
    """
    class RoomCreateForm(forms.ModelForm):
        author = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())

        class Meta:
            model = Room
            fields = ['title', 'slug', 'description', 'scope', 'icon', 'author']

    model = Room
    form_class = RoomCreateForm

    def get_form_kwargs(self):
        if self.request.method == 'POST':
            qd = self.request.POST.copy()
            qd.update({'author_id' : unicode(self.request.user.id)})
            self.request.POST = qd
        return super(RoomCreateView, self).get_form_kwargs()

    def get_form_kwargs(self):
        kwargs = super(RoomCreateView, self).get_form_kwargs()
        if self.request.method == 'POST':
            data = kwargs['data'].copy()
            data['author'] = self.request.user.pk
            kwargs['data'] = data
        return kwargs

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RoomCreateView, self).dispatch(*args, **kwargs)

class RoomDetailView(DetailView):
    """
    View class that shows details for each rooms.
    """
    model = Room

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RoomDetailView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        room = self.get_object()
        user = self.request.user
        if not room.is_viewable(user) and not room.is_joinable(user):
            return HttpResponseForbidden('Permission Denied')
        if not room.is_member(user):
            room.add_member(user)
        return super(RoomDetailView, self).get(request, *args, **kwargs)