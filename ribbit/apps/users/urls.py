from django.conf.urls import patterns, include, url

from views import UserCreateView, UserUpdateView, UserDetailView, UserListView

urlpatterns = patterns('rooms.views',
    url(r'^$', UserListView.as_view(), name='users_user_list'),
    url(r'^signup/$', UserCreateView.as_view(), name='users_user_create'),
    url(r'^update/$', UserUpdateView.as_view(), name='users_user_update'),
    url(r'^(?P<username>[\w-]+)/$', UserDetailView.as_view(), name='users_user_detail'),
)