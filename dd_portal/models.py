from django.db                  import models
from django.contrib.auth.models import AbstractUser, UserManager
from tinymce.models             import HTMLField
from django.db.models.signals   import post_save
from django.core.exceptions     import DoesNotExist

# Note:
# A standard Django user contains by default:
#   * a username
#   * a password
#   * an email
#   * a first name
#   * a last name


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
    #objects = ParentManager()
    # parentprofile = models.OneToOneField(ParentProfile, editable=False, null=True)

    def save(self, force_insert=False, force_update=False):
        super(AbstractUser, self).save(force_insert, force_update)
        try:
            self.parentprofile
        except ParentProfile.DoesNotExist:
            profile = ParentProfile()
            profile.save()
            self.parentprofile = profile
        super(AbstractUser, self).save(force_insert, force_update)

    class Meta:
        verbose_name = 'Parent'

class ParentProfile(models.Model):
    '''
    A  parent profile has a foreign key relationship to:
    * a list of students
    '''
    parent      = models.OneToOneField(Parent, editable=False, null=True)
    ice_contact = models.CharField('In case of emergency', max_length=255, default='<MISSING>')
    notes       = HTMLField('General notes', blank=True)

    def __unicode__(self):
        return self.parent.full_name() or self.parent.username()


class StudentProfile(models.Model):
    '''
    A student profile has:
    * a link to a Django user
    * a single parent account linked to it
    * any number of courses
    * a school grade from a list of choices
    '''
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
    #courses      = models.ManyToManyField(Course, through='Progress')
    school_grade = models.CharField('School grade', \
        max_length=2, choices=SCHOOL_GRADE_CHOICES, default='active')

    def __unicode__(self):
        return self.student.full_name() or self.student.username()

class Student(AbstractUser):
    '''
    A student profile has:
    * a link to a Django user
    * a single parent account linked to it
    * any number of courses
    * a school grade from a list of choices
    '''
    profile = models.OneToOneField(StudentProfile, editable=False)
    parent  = models.ForeignKey(Parent, null=True)

    @classmethod
    def create(cls, username, email, password, parent):
        student = cls(username, email, password, parent)
        student.profile = StudentProfile.create(student=student)
        return student

    class Meta:
        verbose_name = 'Student'


class Progress(models.Model):
    '''
    The relation between a student and a course.

    Contains:
    * the grade results for the student
    * the student's status within the course from a list of choices
    '''
    COURSE_STATUS_CHOICES = (
        ('active'   , 'Active'   ),
        ('dropped'  , 'Dropped'  ),
        ('completed', 'Completed'),
    )
    student = models.ForeignKey(StudentProfile)
    course  = models.ForeignKey(Course)
    status  = models.CharField('Status', \
        max_length=16, choices=COURSE_STATUS_CHOICES, default='05')
    # grades

    class Meta:
        verbose_name        = "Student's progress"
        verbose_name_plural = "Students' progress"


