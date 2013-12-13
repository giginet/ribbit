from django.conf.urls import patterns, include, url

from django.contrib import admin

from ribbit.views import LoginView, LobbyView, IndexView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ribbit.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^rooms/', include('rooms.urls')),
    url(r'^login/$', LoginView.as_view(), name='ribbit_login'),
    url(r'^lobby/$', LobbyView.as_view(), name='ribbit_lobby'),
    url(r'^$', IndexView.as_view(), name='ribbit_index')
)
