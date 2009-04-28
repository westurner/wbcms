# Create your views here.
from django.core.urlresolvers import reverse

from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object, delete_object, lookup_object
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import redirect_to
from django.template import RequestContext
from django.forms.models import inlineformset_factory
from django.template import loader
from django.http import Http404, HttpResponse, HttpResponseRedirect

from tiger.forms import *
from tiger.models import *

from profiles.views import create_profile

from django.utils.translation import ugettext as _

from functools import partial

# Courses

def course_list(request):
    return object_list(request, Course.objects.filter(status__gt=0))

def course_detail(request, id=None, slug=None):
    queryset=Course.objects.filter(status__gt=0)

    return object_detail(request, queryset=queryset, slug_field='slug', slug=slug)

# Course Requests

@login_required
def course_request_create(request,slug):
    """
    File a course request for a given course
    
    
     1. Login (#4) or Register (#3)
     2. Create/Update Profile
     3. Create/Update Course Request
        - + Course
        - + Number of Students
        - + Availability
        - -> Submit
        - = Status[-1]: Unverified
        - Verify Request
           - -> Modify Request (B.3)
           - -> Cancel -> Alert(Confirm: yes/no)
           - -> Submit   
           - = Status[1] Pending
        - Thank You + Email Confirm
           - Course Request
           - -> Course Catalog
           - -> Outstanding Course Requests

    """
    
    initial_form_data = {}

    course = lookup_object(Course, None, slug, 'slug')                 
    initial_form_data['course'] = course.id


    # Lookup profile or redirect to create_profile
    try:
        person = request.user.get_profile()
        initial_form_data['person'] = person.id
    except:
        return create_profile(request, success_url=reverse('course_request_create',args=[course.slug]))
              

    
    model, form_class = CourseRequest, CourseRequestForm
    
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES,initial=initial_form_data,
            min_students=course.min_required_students)

        if form.is_valid():
            new_course_request = form.save(commit=False)
            new_course_request.person = person
            new_course_request.course = course
            new_course_request.save()
            
            request.user.message_set.create(message=_("S The %(verbose_name)s was created successfully.") % {"verbose_name": model._meta.verbose_name})
            return redirect_to(request,reverse('course_request_detail',args=[new_course_request.id]))
    else:
        form = form_class(initial=initial_form_data)

    # Create the template, context, response
    template_name = "%s/%s_form.html" % (model._meta.app_label, model._meta.object_name.lower())
    t = loader.get_template(template_name)
    c = RequestContext(request, {
        'form': form,
        'course':course
    })
    return HttpResponse(t.render(c))

@login_required
def course_request_detail(request, id=None, slug=None):
    queryset=CourseRequest.objects.filter()
    return object_detail(request, queryset=queryset, object_id=id)

@login_required
def course_request_list(request):
    try:
        person = request.user.get_profile()
    except:
        request.user.message_set.create(message=_("S Please update your account information."))
        return create_profile(request, success_url=reverse('course_request_list'))
    return object_list(request, CourseRequest.objects.filter(person=person))

@login_required
def course_request_update(request):
    return update_object(request, form_class=CourseRequestForm)



