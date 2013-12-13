from django.conf.urls import patterns, include, url

from django.contrib import admin

from users.views import LoginView
from ribbit.views import LobbyView, IndexView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rooms/', include('rooms.urls')),
    url(r'^login/$', LoginView.as_view(), name='users_login'),
    url(r'^lobby/$', LobbyView.as_view(), name='ribbit_lobby'),
    url(r'^$', IndexView.as_view(), name='ribbit_index')
)
