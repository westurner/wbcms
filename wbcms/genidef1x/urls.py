from django.conf.urls.defaults import *

from genidef1x import views

urlpatterns = patterns('',
    (r'^docs/(?P<app>\w+)$', views.generate_docs)
)
