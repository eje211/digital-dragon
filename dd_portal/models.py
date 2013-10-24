from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    '''
    A student profile has:
    * a link to a Django user
    * a single parent accound linked to it
    * any number of classes
    * a school grade (for an enum)
    TODO: make sure that a student can never be both actively in a course and
          dropped from it.
    '''
    user            = models.OneToOneField(User)
    parent          = models.ForeignKey(Parent)
    active_courses  = models.ManyToManyField(Course, related_name='active_enrolment')
    dropped_courses = models.ManyToManyField(Course, related_name='dropped_enrolment')
    grade           = models.ForeignKey(Grade)


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
    '''
    pass
    # name
    # description


class Grade(model.Grade):
    '''
    A regular school grade to be used in student profiles.
    '''
    pass
    # name

