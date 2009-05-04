from django.db import models
from django.contrib.localflavor.us import models as us_models
from django.contrib.auth.models import User

import locale
locale.setlocale( locale.LC_ALL, '' )

from django_extensions.db.models import TimeStampedModel
from django_extensions.db.fields import UUIDField

class Company(models.Model):
    """
    A company a ``Person`` may work for.
    """
    name = models.CharField(verbose_name="Company Name", max_length=128)

    def __unicode__(self):
        return self.name
   
    class Meta:
        verbose_name_plural = "Companies"


class Person(TimeStampedModel):
    """
    A person. With name, ``Company``, address, and person information
    """
    first_name = models.CharField(verbose_name="First Name", max_length=42)
    middle_name = models.CharField(verbose_name="Middle Name", max_length=42,
        blank=True)
    last_name = models.CharField(verbose_name="Last Name", max_length=42)
    company = models.ForeignKey('Company', verbose_name="Company",
        related_name="person_worksfor_company",
        blank=True,null=True)
    addr_1 = models.CharField(verbose_name="Address Line 1", max_length=42,
        blank=True)
    addr_2 = models.CharField(verbose_name="Address Line 2", max_length=42,
        blank=True)
    city = models.CharField(verbose_name="City", max_length=42)
    state = us_models.USStateField(verbose_name="State")
    zip_code = models.CharField(verbose_name="Zip Code",
        max_length=10)
    email = models.EmailField(verbose_name="Email Address")
    user = models.ForeignKey(User,unique=True,verbose_name="User",blank=True,
        null=True)


    def __unicode__(self):
        return self.full_name()

    class Meta:
        verbose_name_plural = "People"

    @models.permalink
    def get_absolute_url(self):
        return ('profiles_profile_detail' (), {'username':self.user.username})
        
    def full_name(self):
        return "%s %s %s" % (self.first_name,
            self.middle_name and ('%s.' % self.middle_name) or '',
            self.last_name)
    


class Instructor(Person):
    """
    An instructor. Subclass of ``Person``
    """
    courses = models.ManyToManyField('Course', 
        related_name="ability_to_teach")
        
    def num_courses(self):
      return len(self.courses)
      
    def availability_entries(self):
        return self.instructoravailability_set.count()


class Student(Person):
    """
    A student. Subclass of ``Person``
    """
    pass


PHONE_TYPES = (
    ('business','Business'),
    ('cell','Cell'),
    ('home','Home')
)
class Phone(TimeStampedModel):
    """
    A phone number for a ``Person``
    """
    person = models.ForeignKey('Person',
        related_name="phone_for_person")
    phone_type = models.CharField(verbose_name="Phone Type",max_length="10",
        choices=PHONE_TYPES)
    phone_number = us_models.PhoneNumberField(verbose_name="Phone Number",
        help_text="555-555-5555")
 

class TimeWindow(TimeStampedModel):
    """
    A generic period of time between start and end. May be open or not open.
    Abstract base class.
    """
    start = models.DateTimeField(verbose_name="Start")
    end = models.DateTimeField(verbose_name="End")
    #scheduled = models.BooleanField(verbose_name="status",
    #    help_text="Whether the availability window has been scheduled",
    #    default=False)

    def __unicode__(self):
        return "%s -> %s" % (self.start.strftime("%D %l:%M %p"),
                             self.end.strftime("%D %l:%M %p"))
    
    class Meta:
        abstract = True
        verbose_name = "Time Window"
        verbose_name_plural = "Time Windows"
 

class InstructorAvailability(TimeWindow):
    """
    When an ``Instructor`` is available for teaching
    """
    instructor = models.ForeignKey(Instructor, verbose_name="Instructor")

    class Meta:
        verbose_name_plural = verbose_name = "Instructor Availability"


#class ClientAvailability(TimeWindow):
#    """
#    When a ``Person`` is available to take a course
#    """
#    person = models.ForeignKey(Person, verbose_name="Client")
#    course_request = models.ForeignKey('CourseRequest',
#        verbose_name="Course Request")
#
#    class Meta:
#        verbose_name_plural = verbose_name = "Client Availability"


COURSE_STATUSES = (
   (-3, "Requested"),
   (-2, "Proposed"),
   (-1, "Draft"),
   ( 1, "Available")
)
class Course(TimeStampedModel):
    """
    A ``course`` list entry
    """
    name = models.CharField(verbose_name="Course Name", max_length=256,
    help_text="The course title")
    slug = models.SlugField()
    subject = models.CharField(verbose_name="Course Subject", max_length=128,
    help_text="Course Subject. ex: SOA & BPM")
    description = models.TextField(verbose_name="Course Description",
    help_text="Course description")
    duration = models.CharField(verbose_name="Course Duration", max_length=64,
    help_text="Course Duration")
    cost=models.DecimalField(verbose_name="Course Cost",
        help_text="Cost per person",
        decimal_places=2,
        max_digits=8,
        null=True,
        blank=True)
    min_required_students = models.IntegerField(
        verbose_name="Minimum number of students",
        blank=True)

    status = models.IntegerField(verbose_name="Course Status",
                          choices=COURSE_STATUSES,
                          default=-1)

    def _student_count(self):
        raise NotImplementedError

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('tiger.views.course_request_create',[self.slug])


COURSE_REQUEST_STATUSES = (
            (-1, 'Unverified'),
            ( 1, 'Verified'),    # Pending
            ( 2, 'Deferred'), # Waiting List
            ( 3, 'Scheduled'), # Has a Session
            ( 4, 'Cancelled - By Client'),
            ( 5, 'Cancelled - Duplicate')
)
class CourseRequest(TimeStampedModel):
    """
    A request made by (or on behalf of) a ``Client``, who would like to
    schedule a ``CourseSession``.
    """
    id = UUIDField(primary_key=True)
    person = models.ForeignKey(Person, verbose_name="Client",
        help_text="Client that course request was filed by or on behalf of")
    course = models.ForeignKey(Course, verbose_name="Requested Course")
    number_of_students = models.IntegerField(verbose_name="Number of Students")
    availability_start = models.DateTimeField(verbose_name="Start",blank=True,
        null=True,
        help_text="Availability start date (optional)")
    availability_end = models.DateTimeField(verbose_name="End",blank=True,
        null=True,
        help_text="Availability end date (optional)")
    status = models.IntegerField(verbose_name="Request Status",
        choices=COURSE_REQUEST_STATUSES, default=-1,
        help_text="Course Request Status")
    session = models.ForeignKey('CourseSession',
        verbose_name="Course Session",
        related_name="course_request",
        null=True,
        blank=True)

    def __unicode__(self):
        return u"%s (%s)" % (self.course.name, self.person.full_name())

    @models.permalink
    def get_absolute_url(self):
        return ('tiger.views.course_request_create',[self.id])

    def get_potential_revenue(self):
        return '$%s' % (self.course.cost*self.number_of_students)

    def potential_revenue(self):
        return '%s (%s @ $%s)' % (self.get_potential_revenue(),self.number_of_students, self.course.cost)

    class Meta:
        verbose_name = "Course Request"


class CourseSession(TimeWindow):
    """
    A scheduled ``CourseRequest`` with an ``Instructor`` and one or more
    ``CourseSession``s. Subclass of ``CourseRequest``
    """
    course = models.ForeignKey(Course,
        verbose_name="Course",
        related_name="schedule_for_course")
    instructor = models.ForeignKey(Instructor,
        verbose_name="Instructor",
        related_name="assigned_instructor")
    students = models.ManyToManyField(Student,
        verbose_name="Course Students",
        related_name="student_courseschedule")
    location = models.TextField(verbose_name="Location")
    description = models.TextField(verbose_name="Description")

    def _number_of_students(self):
        return self.students.count()

    def __str__(self):
        return "%s (%s)" % (course.name, instructor.full_name())

    def revenue(self):
        return locale.currency(self.course.cost*self._number_of_students(),
            grouping=True)

    class Meta:
        verbose_name = "Course Session"
