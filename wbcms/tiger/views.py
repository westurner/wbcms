# Create your views here.
from django.core.urlresolvers import reverse
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object, delete_object, lookup_object
from django.views.generic.simple import redirect_to
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext as _

from tiger.forms import *
from tiger.models import *
from profiles.views import create_profile

# Courses

def course_list(request):
    """
    Select and show all active :model:`tiger.Course` objects
    """
    return object_list(request, Course.objects.filter(status__gt=0).order_by('subject'))

def course_detail(request, id=None, slug=None):
    """
    Select and show a :model:`tiger.Course`
    """
    queryset=Course.objects.filter(status__gt=0)
    return object_detail(request, queryset=queryset, slug_field='slug', slug=slug)

# Course Requests

def course_request_create(request,slug):
    """
    File a :model:`tiger.CourseRequest` for a given :model:`tiger.Course`
    """
    
    initial_form_data = {}

    if not request.user.is_authenticated():
        request.flash["messages"] = [("S Please login or create an account to request this course")]
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    course = lookup_object(Course, None, slug, 'slug')                 
    initial_form_data['course'] = course.id

    # Lookup profile or redirect to create_profile
    try:
        person = request.user.get_profile()
        initial_form_data['person'] = person.id
    except:
        request.flash["messages"] = [("S First, we'll need some contact information to contact you about your request")]
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
        'object':course
    })
    return HttpResponse(t.render(c))

@login_required
def course_request_detail(request, id=None, slug=None):
    """
    Select and show a :model:`tiger.CourseRequest` object
    """
    queryset=CourseRequest.objects.select_related()
    return object_detail(request, queryset=queryset, object_id=id)

@login_required
def course_request_list(request):
    """
    Select and show all :model:`tiger.CourseRequest` objects
    """
    try:
        person = request.user.get_profile()
    except:
        request.flash["messages"] = [_("S Please update your contact information.")]
        return create_profile(request, success_url=reverse('course_request_list'))
        
    return object_list(request, CourseRequest.objects.filter(status__gt=0,person=person))

@login_required
def course_request_update(request, id):
    """
    Update a :model:`tiger.CourseRequest` object
    """
    return update_object(request, object_id=id, form_class=CourseRequestForm,
        post_save_redirect=reverse('course_request_detail', args=[id]))

@login_required
def course_request_cancel(request, id):
    """
    Update a :model:`tiger.CourseRequest` object
    """
    course_request = lookup_object(CourseRequest, id, None, None)  
    
    if course_request.session:
        request.flash["messages"] = [_("S This course is scheduled. Please contact us")]
    else:            
        # Set status to cancelled - by client
        course_request.status = -2
        course_request.save()
        request.flash["messages"] = [_("S Your course request has been cancelled")]    
    
    # TODO: Confirm CSRF
    
    return HttpResponseRedirect(reverse('profiles.views.profile_detail', args=[request.user.username]))
    

