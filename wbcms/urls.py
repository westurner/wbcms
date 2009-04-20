from django.conf.urls.defaults import *

import settings
import utils.views

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^users/', include('registration.urls')),
    (r'^accounts/', include('profiles.urls')),
    
    (r'^login$', utils.views.login),
    url(r'^logout/$', auth_views.logout,
        {'template_name': 'registration/logout.html'}),
    
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/gen/', include('genidef1x.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')), 

    # Uncomment the next line to enable the admin:

        
    (r'^admin/(.*)', admin.site.root),
    
    (r'^', include('wbcms.tiger.urls')),
)

if settings.DEBUG:
    from django.contrib import databrowse
    from tiger.models import *
    databrowse.site.register(Person)
    databrowse.site.register(Course)
    databrowse.site.register(CourseRequest)
    urlpatterns += patterns('',
        (r'^db/(.*)', login_required(databrowse.site.root)),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
        )
