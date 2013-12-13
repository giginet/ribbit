from django.conf.urls import patterns, include, url

from django.contrib import admin

from ribbit.views import IndexView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ribbit.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', IndexView.as_view())
)
