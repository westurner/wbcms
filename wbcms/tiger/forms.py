from django import forms
from django.forms import ModelForm
from tiger.models import *
    
from django.contrib.admin.widgets import AdminDateWidget, AdminSplitDateTime

    
class CourseRequestForm(forms.Form):
    #person = forms.ModelChoiceField(queryset=Person.objects.all(),label=u'Client',widget=forms.HiddenInput())
    #course = forms.ModelChoiceField(queryset=Course.objects.all(), label=u'Requested Course')
    number_of_students = forms.IntegerField(label=u'Number of Students',
        error_messages={'required':'Please enter the number of students',
                        'invalid':'Please enter a whole number'})
                        
    availability_start = forms.DateTimeField(label=u'Start',
        widget=AdminDateWidget(),
        error_messages={'required':'Please enter an availability start date',
                        'invalid':'Please enter a date in the format YYYY-MM-DD'})
    availability_end = forms.DateTimeField(label=u'End',
        widget=AdminDateWidget(),
        error_messages={'required':'Please enter an availability end date',
                        'invalid':'Please enter a date in the format YYYY-MM-DD'})
    #status = forms.TypedChoiceField(initial=-1, label=u'Request Status')
    #session = forms.ModelChoiceField(queryset=CourseSession.objects.all(),
    #    required=False, label=u'Course Session')
        
    def save(self):
        pass
        
    class Meta:
        model = CourseRequest


class CourseRequestForm(forms.ModelForm):
    class Meta:
        model = CourseRequest
        fields = ('number_of_students','availability_start','availability_end')
        
    def __init__(self, *args, **kwargs):
        self.min_students = kwargs.pop('min_students',0)
        super(CourseRequestForm, self).__init__(*args, **kwargs)
        self.fields['availability_start'].widget = AdminDateWidget()
        self.fields['availability_start'].error_messages = {
             'required':'Please enter an availability start date',
             'invalid':'Please enter a date in YYYY-MM-DD format'}
        self.fields['availability_end'].widget = AdminDateWidget()
        self.fields['availability_end'].error_messages = {
             'required':'Please enter an availability end date',
             'invalid':'Please enter a date in YYYY-MM-DD format'}

        
    def clean_number_of_students(self):
        requested_students = int(self.cleaned_data['number_of_students'])
        min_students = self.min_students
        
        if requested_students > min_students:
            return requested_students
        raise forms.ValidationError("This course has a minimum number of students (%s)" % min_students)


#class CourseRequestForm(ModelForm):
#    class Meta:
#        model = CourseRequest
#        fields = ('course','person','number_of_students','availability_start','availability_end')

class ProfileForm(ModelForm):
    class Meta:
        model = Person
        
