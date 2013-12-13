from django.shortcuts import render

from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from rooms.models import Room

"""
View class that to create
"""
class RoomCreateView(CreateView):
    model = Room

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RoomCreateView, self).dispatch(*args, **kwargs)

"""
View class that shows details for each rooms.
"""
class RoomDetailView(DetailView):
    model = Room

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RoomDetailView, self).dispatch(*args, **kwargs)