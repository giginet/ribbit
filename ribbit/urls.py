from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin

from apps.users.views import LoginView
from ribbit.views import LobbyView, IndexView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rooms/', include('ribbit.apps.rooms.urls')),
    url(r'^api/', include('ribbit.apps.apis.routers')),
    url(r'^login/$', LoginView.as_view(), name='users_login'),
    url(r'^lobby/$', LobbyView.as_view(), name='ribbit_lobby'),
    url(r'^$', IndexView.as_view(), name='ribbit_index')
)
urlpatterns += staticfiles_urlpatterns()
