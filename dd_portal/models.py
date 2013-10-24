from django.db import models
from django.contrib.auth.models import User

# Note:
# A standard Django user contains by default:
#   * a username
#   * a password
#   * an email
#   * a first name
#   * a last name

class Student(models.Model):
    '''
    A student profile has:
    * a link to a Django user
    * a single parent accound linked to it
    * any number of courses
    * a school grade from a list of choices
    '''
    user    = models.OneToOneField(User)
    parent  = models.ForeignKey(Parent)
    courses = models.ManyToManyField(Course, through=Progress)
    # school_grade from COURSE_STATUS_CHOICES


class Parent(models.Model):
    '''
    A parent profile has:
    * a link to a Django user

    Furthermore, parent profile has a foreign key relationship to:
    * a list of students
    '''
    user = models.OneToOneField(User)


class Course(model.Model):
    '''
    A course has:
    * a name
    * a description

    Furthermore, a course is linked by a many-to-many relationship with:
    * a list of current students
    * a list of dropped students
    * a list of students having completed it
    '''
    pass
    # name
    # description


class Progress(models.Model):
    '''
    The relation between a student and a course.

    Contains:
    * the grade results for the student
    * the student's status within the course from a list of choices
    '''
    student = models.ForeignKey(Student)
    course  = models.ForeignKey(Course)
    # status from COURSE_STATUS_CHOICES
    # grades


SCHOOL_GRADE_CHOICES = (
    ('5' , 'Middle Freshman'),
    ('6' , 'Middle Sophomore'),
    ('7' , 'Middle Junior'),
    ('8' , 'Middle Senior'),
    ('9' , 'High Freshman'),
    ('10', 'High Sophomore'),
    ('11', 'High Junior'),
    ('12', 'High Senior'),
)

COURSE_STATUS_CHOICES = (
    ('active'   , 'Active'),
    ('dropped'  , 'Dropped'),
    ('completed', 'Completed'),
)
