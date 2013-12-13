from django.conf.urls import patterns, include, url

from django.contrib import admin

from rooms.views import RoomCreateView, RoomDetailView
from ribbit.views import IndexView

urlpatterns = patterns('rooms.views',
    url(r'^create/$', RoomCreateView.as_view(), name='rooms_room_create'),
    url(r'^(?P<pk>\d+)/$', RoomDetailView.as_view(), name='rooms_room_detail'),
)