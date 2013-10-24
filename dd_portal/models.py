from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    '''
    A student profile has:
    * a single parent accound linked to it
    * any number of classes
    * a school grade (for an enum)
    '''
    user = models.OneToOneField(User)
    # parent
    # classes
    # grade

class Parent(models.Model):
    '''
    A parent profile has:
    * any number of student accounts linked to it.
    '''
    user = models.OneToOneField(User)
    # student

class Course(model.Model):
    '''
    A course has:
    * a name
    * a description
    * a list of current students
    * a list of dropped students
    '''
    pass
    # name
    # description
    # students
    # dropped students

