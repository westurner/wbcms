from django.conf.urls.defaults import *
from django.contrib import admin

from tiger.views import course_request_create, course_request_update
from tiger.views import course_list, course_detail
from tiger.views import *
from tiger.models import *

#admin.autodiscover()

urlpatterns = patterns('',

        # Courses
        url(r'courses/$',
            course_list,
            name='course_list'),

        # Course Requests
        url(r'courses/(?P<slug>[\w-]+)/$',
            course_request_create,
            name='course_request_create'),
        url(r'requests/$',
            course_request_list,
            name='course_request_list'),
        url('requests/(?P<id>[\w-]+)/$',
            course_request_detail,
            name='course_request_detail'),
        url(r'requests/create/$',
            course_request_create,
            name='course_request_create_blank'),
        url(r'requests/(?P<id>[\w-]+)/update/$',
            course_request_update,
            name='course_request_update'),
        url(r'requests/(?P<id>[\w-]+)/cancel/$',
            course_request_cancel,
            name='course_request_cancel'),

)


