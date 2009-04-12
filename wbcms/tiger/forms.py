from django.forms import ModelForm
from wbcms.tiger.models import CourseRequest, Person

class CourseRequestForm(ModelForm):
    class Meta:
        model = CourseRequest
        fields = ('course','number_of_students',)

class ProfileForm(ModelForm):
    class Meta:
        model = Person
        
