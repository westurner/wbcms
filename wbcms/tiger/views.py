# Create your views here.
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
    """
    
    # try to get the course by slug
    try:
        course = lookup_object(Course, None, slug, 'slug')
        initial = {'course':course.id}
    except:
        return redirect_to('/courses')
    
    model, form_class = CourseRequest, CourseRequestForm
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES,initial=initial)
        if form.is_valid():
            new_object = form.save()
            if request.user.is_authenticated():
                request.user.message_set.create(message=ugettext("The %(verbose_name)s was created successfully.") % {"verbose_name": model._meta.verbose_name})
            return redirect(post_save_redirect, new_object)
    else:
        form = form_class(initial=initial)

    # Create the template, context, response
    template_name = "%s/%s_form.html" % (model._meta.app_label, model._meta.object_name.lower())
    t = loader.get_template(template_name)
    c = RequestContext(request, {
        'form': form,
    })
    return HttpResponse(t.render(c))
    
    
    # create a form for the course request
    #CourseRequestForm(initial={'course':course.id})
    
    #from django.forms.models import modelformset_factory
    #CourseRequestFormSet = modelformset_factory(CourseRequest)
    #formset = CourseRequestFormSet(queryset=
    
    #BookFormSet = inlineformset_factory(Course, Book)
    #author = Author.objects.get(name=u'Mike Royko')
    #formset = BookFormSet(instance=author)
    #return create_object(request, model=CourseRequest, form_class=CourseRequestForm)

@login_required
def course_request_update(request):
    return update_object(request, form_class=CourseRequestForm)



