from django.contrib import admin
from wbcms.tiger.models import *

class PhoneInline(admin.TabularInline):
    model = Phone

    verbose_name = "Phone Number"


class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','company','email',)
    inlines = [PhoneInline]

    verbose_name_plural = "People"


class InstructorAvailabilityInline(admin.TabularInline):
    model = InstructorAvailability

    verbose_name = "Availability"
    verbose_name_plural = "Availability"


class InstructorAdmin(admin.ModelAdmin):
    inlines = [PhoneInline, InstructorAvailabilityInline ]


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name','subject',)
    prepopulated_fields = {'slug': ('name',) }


class ClientAvailabilityInline(admin.TabularInline):
    model = ClientAvailability


class CourseRequestAdmin(admin.ModelAdmin):
    list_display = ('person', )

    inlines = [ ClientAvailabilityInline ]


class CourseScheduleAdmin(admin.ModelAdmin):
    list_display = ['course','instructor','_number_of_students']


admin.site.register(Company)
admin.site.register(Person,PersonAdmin)
admin.site.register(Instructor,InstructorAdmin)
admin.site.register(InstructorAvailability)
admin.site.register(ClientAvailability)
admin.site.register(Course,CourseAdmin)
admin.site.register(CourseRequest,CourseRequestAdmin)
admin.site.register(CourseSchedule, CourseScheduleAdmin)

