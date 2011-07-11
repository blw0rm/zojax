### -*- coding: utf-8 -*- ####################################################

from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

#from django.views.generic.simple import direct_to_template


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include("django.contrib.auth.urls")),
    url(r'^auth/', include('publicauth.urls')),
)

urlpatterns += patterns('zojax.views',

    url(r'^$', "index", name="index"),
    url(r'^document/delete/(\d+)/$', "remove_document", name="remove_document"),
    url(r'^document/share/(\d+)/$', "share_document", name="share_document"),
    url(r'^document/(\d+)/$', "view_document", name="view_document"),


)

urlpatterns += staticfiles_urlpatterns()