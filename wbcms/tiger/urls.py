from django.conf.urls.defaults import *
from django.contrib import admin

from tiger.views import course_request_create, course_request_update
from tiger.views import course_list, course_detail
from tiger.views import *
from tiger.models import *


# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
        url(r'requests/add', 'tiger.views.course_request_create'),
        url(r'requests/update', 'tiger.views.course_request_update'),
        url(r'courses/$', 'tiger.views.course_list'),
        url(r'courses/(?P<slug>[\w-]+)$', 'tiger.views.course_detail'),
        url(r'courses/(?P<slug>[\w-]+)/request', 'tiger.views.course_request_create'),

    #(r'^wbcms/', include('wbcms.tiger.urls')),
)
