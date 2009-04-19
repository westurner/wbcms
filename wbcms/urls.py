from django.conf.urls.defaults import *

import settings
import utils.views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.auth import views as auth_views
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^accounts/', include('registration.urls')),
    (r'^profiles/', include('profiles.urls')),
    
    (r'^login$', utils.views.login),
    url(r'^logout/$', auth_views.logout,
        {'template_name': 'registration/logout.html'}),
    
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/gen/', include('genidef1x.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')), 

    # Uncomment the next line to enable the admin:
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
        
    (r'^admin/(.*)', admin.site.root),
    (r'^', include('wbcms.tiger.urls')),
)
