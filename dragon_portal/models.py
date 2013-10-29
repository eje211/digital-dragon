from django.db                  import models
from django.contrib.auth.models import UserManager, AbstractUser
from tinymce.models             import HTMLField    

# Note:
# A standard Django user contains by default:
#   * a username
#   * a password
#   * an email
#   * a first name
#   * a last name

# class UsernameRefField(models.Field):
#     name         = None
#     verbose_name = 'Username'
#     db_column    = None
#     db_type      = None
#     rel          = None
#     primary_key  = None
#     _choices     = None
#     db_index     = None
#     editable     = False
#     default      = ''
#     def __init__(self): pass
#     def to_python(self, value):
#         return self.dragonuser.username

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


class DragonUserManager(UserManager):

    def create_user(self, *args, **kwargs):
        """
        """
        self.model = DragonUser
        user = UserManager.create_user(self, *args, **kwargs)
        if user.user_type == 'admin': return user
        try:
            profileType = globals()[capitalize(self.user_type) + 'Profile']
        except KeyError:
            print('No profile type for user of type: %s' % user.user_type)
        else:
            myProfile = profileType.objects.filter(user_id=self.id)
            if not len(myProfile): myProfile.create(user=self.id)
        return user


class ParentProfile(models.Model):
    '''

    '''
 #    username    = UsernameRefField()
    ice_contact = models.CharField('In case of emergency', max_length=255, \
        default='<MISSING>')
    notes       = HTMLField('General notes', blank=True)

    def __unicode__(self):
        return self.dragonuser.full_name


class StudentProfile(models.Model):
    '''

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
    courses      = models.ManyToManyField(Course, through='Progress')
    parent       = models.ForeignKey(ParentProfile)
    school_grade = models.CharField('School grade', \
        max_length=2, choices=SCHOOL_GRADE_CHOICES, default='active')

    def __unicode__(self):
        return self.dragonuser.full_name


class DragonUser(AbstractUser):
    '''
    A  parent profile has a foreign key relationship to:
    * a list of students
    '''
    USER_TYPE_CHOICES = (
        ('admin'  , 'Administrator'),
        ('parent' , 'Parent'       ),
        ('student', 'Student'      ),
    )
    user_type       = models.CharField('User Type', max_length=16,
        editable=False, choices=USER_TYPE_CHOICES, default='admin')
    student_profile = models.OneToOneField(StudentProfile,
        editable=False, null=True)
    parent_profile  = models.OneToOneField(ParentProfile,
        editable=False, null=True)
    objects = DragonUserManager()

    @property
    def full_name(self):
        return ('%s %s' % (self.first_name, \
            self.last_name)) or self.username


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

