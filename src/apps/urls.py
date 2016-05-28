from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.http import HttpResponseRedirect
from os.path import join, abspath, dirname

urlpatterns = [
    # Examples:
    # url(r'^$', 'apps.views.home', name='home'),

    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/', include('registration.backends.simple.urls')),
    # url(r'^accounts/', include('django.contrib.auth.urls', namespace="auth")),

    url(r'^uks/', include('uks.urls', namespace='uks')),
    url(r'^$', 'apps.views.home'),

    # Examples:
    # url(r'^$', 'upload.views.home', name='home'),

    url(r'^$', lambda x: HttpResponseRedirect('/upload/new/')),
    url(r'^upload/', include('fileupload.urls')),
]

urlpatterns += patterns('',
                        (r'^media/(.*)$', 'django.views.static.serve',
                         {'document_root': join(abspath(dirname(__file__)), 'media')}),
                        )
