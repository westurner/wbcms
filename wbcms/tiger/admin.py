from django.contrib import admin
from wbcms.tiger.models import *

class PhoneInline(admin.TabularInline):
    model = Phone
    verbose_name = "Phone Number"


class PersonAdmin(admin.ModelAdmin):
    list_display = ('last_name','first_name','company','email', 'modified')
    inlines = [PhoneInline]
    list_filter = ('company',)
    verbose_name_plural = "People"
    save_on_top = True


class StudentAdmin(admin.ModelAdmin):
    list_display = ('last_name','first_name','company','email')
    list_filter = ('company',)
    inlines = [PhoneInline]
    save_on_top = True


class InstructorAvailabilityInline(admin.TabularInline):
    model = InstructorAvailability

    list_filter = ('instructor',)
    date_hierarchy = 'availability_start'

    verbose_name = "Availability"
    verbose_name_plural = "Availability"


class InstructorAdmin(admin.ModelAdmin):
    list_display = ('last_name','first_name','email','modified')
    inlines = [PhoneInline, InstructorAvailabilityInline ]
    save_on_top = True


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name','subject','duration','cost','min_required_students')
    list_filter = ('subject','duration')
    search_fields = ('name','subject',)
    prepopulated_fields = {'slug': ('name',) }
    save_on_top = True


#class ClientAvailabilityInline(admin.TabularInline):
#    model = ClientAvailability
#
#    list_filter = ('instructor',)
#    date_hierarchy = 'availability_start'
    

class CourseRequestAdmin(admin.ModelAdmin):
    list_display = ('person','course','status','potential_revenue','created','modified' )
    date_hierarchy = 'created'
    list_filter = ('status',)
    radio_fields = {'status': admin.VERTICAL}

    fieldsets = (
        (None, {
            'fields': ('course','number_of_students','person','availability_start','availability_end')}),
        ('Request Scheduling', {
            'fields': ('status', 'session') }),
    )
    save_on_top = True

    #inlines = [ ClientAvailabilityInline ]


class CourseSessionAdmin(admin.ModelAdmin):
    list_display = ['course','instructor','start','_number_of_students','revenue']
    list_filter = ('instructor',)
    date_hierarchy = 'start'
    list_select_related = True
    filter_horizontal = ('students',)
    save_on_top = True

admin.site.register(Company)
admin.site.register(Person,PersonAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(Instructor,InstructorAdmin)
admin.site.register(InstructorAvailability)
#admin.site.register(ClientAvailability)
admin.site.register(Course,CourseAdmin)
admin.site.register(CourseRequest,CourseRequestAdmin)
admin.site.register(CourseSession, CourseSessionAdmin)

