from django import forms
from django.forms import ModelForm
from tiger.models import *
    
class CourseRequestForm(forms.Form):
    person = forms.ModelChoiceField(queryset=Person.objects.all(),label=u'Client')
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label=u'Requested Course')
    number_of_students = forms.IntegerField(label=u'Number of Students')
    availability_start = forms.DateTimeField(label=u'Start')
    availability_end = forms.DateTimeField(label=u'End')
    status = forms.TypedChoiceField(initial=-1, label=u'Request Status')
    session = forms.ModelChoiceField(queryset=CourseSession.objects.all(),
        required=False, label=u'Course Session')
        
    class Meta:
        model = CourseRequest


class CourseRequestForm(ModelForm):
    class Meta:
        model = CourseRequest
        fields = ('course','number_of_students','availability_start','availability_end')

class ProfileForm(ModelForm):
    class Meta:
        model = Person
        
