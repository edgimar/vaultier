from django.conf.urls import patterns, include, url

from vaultier import settings
from core import urls_api,views
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'vaultier.views.home', name='home'),
    # url(r'^vaultier/', include('vaultier.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:

    # url(r'^testing/$', views.SecurityViewSet.as_view()),

    url(r'^api/', include('core.urls_api')),
    url(r'^admin/', include(admin.site.urls)),

    # Frontend
    url(r'^', include('core.urls')),
)

if settings.DEBUG :
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )