from django import forms
from django.http.response import HttpResponseForbidden
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from ribbit.apps.users.models import User

from ribbit.apps.rooms.models import Room, Role

def room_permission_required(role=Role.MEMBER):
    def _decorator(function):
        def actual(*args, **kwargs):
            view = args[0]
            room = view.get_object()
            user = view.request.user
            results = {
                Role.ADMIN : room.is_administrable(user),
                Role.MEMBER : room.is_member(user),
                Role.VIEWER : room.is_viewable(user)
            }
            if not results[role]:
                return HttpResponseForbidden('Permission Denied')
            return function(*args, **kwargs)
        return actual
    return _decorator

def room_joinable_required(function):
    def _actual(*args, **kwargs):
        view = args[0]
        room = view.get_object()
        user = view.request.user
        if not room.is_joinable(user) and not room.is_member(user):
            return HttpResponseForbidden('Permission Denied')
        return function(*args, **kwargs)
    return _actual

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
    View class which shows details for each rooms.
    """
    model = Room

    @method_decorator(login_required)
    @room_joinable_required
    def dispatch(self, *args, **kwargs):
        return super(RoomDetailView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        room = self.get_object()
        user = self.request.user
        if not room.is_member(user):
            room.add_member(user)
        return super(RoomDetailView, self).get(request, *args, **kwargs)

class RoomUpdateView(UpdateView):
    """
    View class which shows the view to update each rooms.
    """
    model = Room
    fields = ('title', 'description', 'is_active',)

    @method_decorator(login_required)
    @room_permission_required(role=Role.ADMIN)
    def dispatch(self, *args, **kwargs):
        return super(RoomUpdateView, self).dispatch(*args, **kwargs)
