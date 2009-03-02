from django.forms import ModelForm
from wbcms.tiger.models import CourseRequest, Person

class CourseRequestForm(ModelForm):
    fields = ('course','number_of_students',)

    class Meta:
        model = CourseRequest
        
class ProfileForm(ModelForm):
    class Meta:
        model = Person
        
