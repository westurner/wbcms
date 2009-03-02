# Create your views here.
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object, delete_object
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import redirect_to
from django.template import RequestContext

from wbcms.tiger.forms import *
from wbcms.tiger.models import *

#@login_required
def course_request_create(request,slug=None):
    return create_object(request, form_class=CourseRequestForm)

#@login_required
def course_request_update(request):
    return update_object(request, form_class=CourseRequestForm)


def course_list(request):
    return object_list(request, Course.objects.filter(status__gt=0))

def course_detail(request, id=None, slug=None):
    queryset=Course.objects.filter(status__gt=0)

    return object_detail(request, queryset=queryset, slug_field='slug', slug=slug)

def profile_create(request):
    return create_object(request, model=Person)
    
def profile_update(request):
    return update_object(request, model=Person)
    
def profile_detail(request):
    try:
        return object_detail(request, queryset=Person.objects.filter(user__eq=request.user))
    except IndexError:
        return redirect_to('/tiger/profile/new')
