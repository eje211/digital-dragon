from django.db                  import models
from django.contrib.auth.models import AbstractUser
from tinymce.models             import HTMLField

# Note:
# A standard Django user contains by default:
#   * a username
#   * a password
#   * an email
#   * a first name
#   * a last name

SCHOOL_GRADE_CHOICES = (
    ('05', 'Middle Freshman' ),
    ('06', 'Middle Sophomore'),
    ('07', 'Middle Junior'   ),
    ('08', 'Middle Senior'   ),
    ('09', 'High Freshman'   ),
    ('10', 'High Sophomore'  ),
    ('11', 'High Junior'     ),
    ('12', 'High Senior'     ),
)

COURSE_STATUS_CHOICES = (
    ('active'   , 'Active'   ),
    ('dropped'  , 'Dropped'  ),
    ('completed', 'Completed'),
)


class Course(models.Model):
    '''
    A course has:
    * a name
    * a description

    Furthermore, a course is linked by a many-to-many relationship with:
    * a list of students
    '''
    name        = models.CharField('Name', max_length=255)
    description = HTMLField('Description')

    def __unicode__(self):
        return self.name


class Parent(AbstractUser):
    '''
    A  parent profile has a foreign key relationship to:
    * a list of students
    '''
    ice_contact = models.CharField('In case of emergency', max_length=255)
    notes       = HTMLField('General notes', blank=True)

    class Meta:
        verbose_name = 'Parent'


class Student(AbstractUser):
    '''
    A student profile has:
    * a link to a Django user
    * a single parent account linked to it
    * any number of courses
    * a school grade from a list of choices
    '''
    parent       = models.ForeignKey(Parent)
    courses      = models.ManyToManyField(Course, through='Progress')
    school_grade = models.CharField('School grade', \
        max_length=2, choices=COURSE_STATUS_CHOICES, default='active')

    class Meta:
        verbose_name = 'Student'


class Progress(models.Model):
    '''
    The relation between a student and a course.

    Contains:
    * the grade results for the student
    * the student's status within the course from a list of choices
    '''
    student = models.ForeignKey(Student)
    course  = models.ForeignKey(Course)
    status  = models.CharField('Status', \
        max_length=16, choices=COURSE_STATUS_CHOICES, default='05')
    # grades
