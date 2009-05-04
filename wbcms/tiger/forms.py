from django import forms
from tiger.models import *
    
from django.contrib.admin.widgets import AdminDateWidget, AdminSplitDateTime

class CourseRequestForm(forms.ModelForm):
    class Meta:
        model = CourseRequest
        fields = ('number_of_students','availability_start','availability_end')
        
    def __init__(self, *args, **kwargs):
        self.min_students = kwargs.pop('min_students',0)
        super(CourseRequestForm, self).__init__(*args, **kwargs)
        self.fields['availability_start'].label = "Availability Start"
        self.fields['availability_start'].widget = AdminDateWidget()
        self.fields['availability_start'].error_messages = {
             'required':'Please enter an availability start date',
             'invalid':'Please enter a date in YYYY-MM-DD format'}
        self.fields['availability_end'].label = "Availability End"
        self.fields['availability_end'].widget = AdminDateWidget()
        self.fields['availability_end'].error_messages = {
             'required':'Please enter an availability end date',
             'invalid':'Please enter a date in YYYY-MM-DD format'}

        
    def clean_number_of_students(self):
        requested_students = int(self.cleaned_data['number_of_students'])
        min_students = self.min_students
        
        if requested_students >= min_students:
            return requested_students
        raise forms.ValidationError("This course has a minimum number of students (%s)" % min_students)



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Person
        
