from django.contrib import admin
from wbcms.tiger.models import *


class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','company','phone_number','email')


class InstructorAvailabilityInline(admin.TabularInline):
    model = InstructorAvailability

    verbose_name = "Availability"
    verbose_name_plural = "Availability"


class InstructorAdmin(admin.ModelAdmin):
    inlines = [InstructorAvailabilityInline ]


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name','subject')


class ClientAvailabilityInline(admin.TabularInline):
    model = ClientAvailability


class CourseRequestAdmin(admin.ModelAdmin):
    list_display = ('client', 'client')

    inlines = [ ClientAvailabilityInline ]


class CourseSessionInline(admin.TabularInline):
    model = CourseSession

class CourseScheduleAdmin(admin.ModelAdmin):
    list_display = ['course','instructor','_number_of_students','_number_of_sessions']

    inlines = [ CourseSessionInline ]



admin.site.register(Company)
admin.site.register(Contact,ContactAdmin)
admin.site.register(Instructor,InstructorAdmin)
admin.site.register(InstructorAvailability)
admin.site.register(ClientAvailability)
admin.site.register(Course,CourseAdmin)
admin.site.register(CourseRequest,CourseRequestAdmin)
admin.site.register(CourseSession)
admin.site.register(CourseSchedule, CourseScheduleAdmin)

