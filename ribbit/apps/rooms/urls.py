from django.conf.urls import patterns, include, url

from views import RoomCreateView, RoomDetailView, RoomUpdateView, RoomLeaveView

urlpatterns = patterns('rooms.views',
    url(r'^create/$', RoomCreateView.as_view(), name='rooms_room_create'),
    url(r'^(?P<slug>[\w-]+)/$', RoomDetailView.as_view(), name='rooms_room_detail'),
    url(r'^(?P<slug>[\w-]+)/update/$', RoomUpdateView.as_view(), name='rooms_room_update'),
    url(r'^(?P<slug>[\w-]+)/leave/$', RoomLeaveView.as_view(), name='rooms_room_leave'),
)
