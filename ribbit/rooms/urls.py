from django.conf.urls import patterns, include, url

from rooms.views import RoomCreateView, RoomDetailView

urlpatterns = patterns('rooms.views',
    url(r'^create/$', RoomCreateView.as_view(), name='rooms_room_create'),
    url(r'^(?P<pk>\d+)/$', RoomDetailView.as_view(), name='rooms_room_detail'),
)