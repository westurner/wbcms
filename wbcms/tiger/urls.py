from django.conf.urls.defaults import *
from django.contrib import admin

#from tiger.views import course_request_create, course_request_update
#from tiger.views import course_list, course_detail
from tiger.views import *


from tiger.models import *

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
        (r'requests/add', course_request_create ),
        (r'requests/update', course_request_update ),
        (r'courses/$', course_list),
        (r'courses/(?P<slug>[\w-]+)', course_detail),
        (r'courses/(?P<slug>[\w-]+)/request', course_request_create),

    #(r'^wbcms/', include('wbcms.tiger.urls')),
)
