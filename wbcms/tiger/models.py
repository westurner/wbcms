from django.db import models
from django.contrib.localflavor.us import models as us_models
from django.contrib.auth.models import User

class Company(models.Model):
    """
    A company a ``contact`` may work for.
    """
    name = models.CharField(verbose_name="Company Name", max_length=128)

    def __unicode__(self):
        return self.name
   
    class Meta:
        verbose_name_plural = "companies"


class Contact(models.Model):
    """
    A person. With name, ``company``, address, and contact information
    """
    # XXX: Do we need to store multiple addresses, emails, etc?
    first_name = models.CharField(verbose_name="First Name", max_length=42)
    middle_name = models.CharField(verbose_name="Middle Name", max_length=42)
    last_name = models.CharField(verbose_name="Last Name", max_length=42)
    company = models.ForeignKey('Company', verbose_name="Company",
        related_name="contact_worksfor_company")
    addr_1 = models.CharField(verbose_name="Address Line 1", max_length=42,
        blank=True)
    addr_2 = models.CharField(verbose_name="Address Line 2", max_length=42,
        blank=True)
    city = models.CharField(verbose_name="City", max_length=42)
    state = us_models.USStateField(verbose_name="State")
    zip_code = models.CharField(verbose_name="Zip Code", 
        max_length=10)
    phone_number = us_models.PhoneNumberField(verbose_name="Phone Number",
        help_text="555-555-5555")
    email = models.EmailField(verbose_name="Email Address")
    
    def __unicode__(self):
        return "%s %s %s" % (self.first_name, 
            self.middle_name and ('%s.' % self.middle_name) or '',
            self.last_name)


class Instructor(Contact):
    """
    An instructor. Subclass of ``Contact``
    """
    courses = models.ManyToManyField('Course', 
        related_name="instructor_teaches_courses")


class TimeWindow(models.Model):
    """
    A generic period of time between start and end. May be open or not open.
    Abstract base class.
    """
    starting = models.DateTimeField(verbose_name="Start")
    ending = models.DateTimeField(verbose_name="End")
    open = models.BooleanField(verbose_name="Open",
        help_text="Whether the time window is still open",
        default=True)

    def __unicode__(self):
        return "%s -> %s" % (self.starting.strftime("%D %l:%M %p"),
                             self.ending.strftime("%D %l:%M %p"))
    
    class Meta:
        abstract = True
        verbose_name = "Time Window"
        verbose_name_plural = "Time Windows"
 

class InstructorAvailability(TimeWindow):
    """
    When an ``instructor`` is available. Subclass of ``TimeWindow``
    """
    instructor = models.ForeignKey(Instructor, verbose_name="Instructor")

    class Meta:
        verbose_name_plural = verbose_name = "Instructor Availability"


class ClientAvailability(TimeWindow):
    """
    When a ``client`` is available. Subclass of ``TimeWindow``
    """
    client = models.ForeignKey(Contact, verbose_name="Client")
    course_request = models.ForeignKey('CourseRequest',
        verbose_name="Course Request")

    class Meta:
        verbose_name_plural = verbose_name = "Client Availability"

    
class Course(models.Model):
    """
    A ``course`` offered through the TDC
    """
    name = models.CharField(verbose_name="Course Name", max_length=256)
    subject = models.CharField(verbose_name="Course Subject", max_length=128)
    description = models.TextField(verbose_name="Course Description")
    cost=models.DecimalField(verbose_name="Course Cost",
        help_text="Cost per person",
        decimal_places=2,
        max_digits=8,
        null=True,
        blank=True)

    def _student_count(self):
        return 

    def __unicode__(self):
        return self.name


COURSE_REQUEST_STATUSES = (
    ('Pending', (
            (-1, 'Unverified'),
            ( 1, 'Verified'),    # Pending
            ( 2, 'Deferred') )), # Waiting List
    ('Scheduled', (
            ( 3, 'Scheduled'), )),
    ('Cancelled', (
            ( 4, 'Cancelled - By Client'),
            ( 5, 'Cancelled - Duplicate') ))
)
class CourseRequest(models.Model):
    """
    A request made by (or on behalf of) a ``client``, who would like to
    schedule a ``Course``s during one or more periods of ``Availability``.
    """
    client = models.ForeignKey(Contact, verbose_name="Client")
    course = models.ForeignKey(Course, verbose_name="Requested Course")
    number_of_students = models.IntegerField(verbose_name="Number of Students")
    status = models.IntegerField(verbose_name="Request Status",
        choices=COURSE_REQUEST_STATUSES, default=-1)
    schedule = models.ForeignKey('CourseSchedule',
        verbose_name="Course Schedule",
        related_name="scheduled_course_request",
        null=True,
        blank=True)

    class Meta:
        verbose_name = "Course Request"


class CourseSession(TimeWindow):
    """
    A course session with a location, description, and a note for the
    training coordinator. Subclass of ``TimeWindow``.
    """
    location = models.TextField(verbose_name="Session Location")
    description = models.TextField(verbose_name="Session Description")
    notes = models.TextField(verbose_name="Session Notes")
    schedule = models.ForeignKey('CourseSchedule',
        verbose_name="Course Schedule",
        related_name="course_schedule_sessions")

    class Meta:
        verbose_name = "Course Session"


class CourseSchedule(models.Model):
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
    students = models.ManyToManyField(Contact,
        verbose_name="Course Students",
        related_name="student_takes_course")

    def _number_of_students(self):
        return self.students.count()

    def _number_of_sessions(self):
        return self.course_schedule_sessions.count()

    class Meta:
        verbose_name = "Course Schedule"
    

# XXX: On the web course request form, a "would you be interested in" survey
# could generate additional warm leads
# XXX: Costs? Per Course
