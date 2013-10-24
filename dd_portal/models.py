from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    '''
    A student profile has:
    * a link to a Django user
    * a single parent accound linked to it
    * any number of active courses
    * any number of dropped courses
    * any number of completed courses
    * a school grade (for an enum)
    TODO: make sure that a student can only ever be in one of actively in a
          crourse, dropped from it or having completed it.
    '''
    user              = models.OneToOneField(User)
    parent            = models.ForeignKey(Parent)
    active_courses    = models.ManyToManyField(Course, through=Results)
    dropped_courses   = models.ManyToManyField(Course, through=OnHold)
    completed_courses = models.ManyToManyField(Course, through=Summary)
    grade             = models.ForeignKey(SchoolGrade)


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
    Abstract class that contains the relation between a student and their
    course.
    Additionally, this relation contains the grade results for the student
    in that course.
    '''
    student = models.ForeignKey(Student)
    course  = models.ForeignKey(Course)
    # grades

class Results(Progress):
    pass

class OnHold (Progress):
    pass

class Summary(Progress):
    pass

class SchoolGrade(model.Grade):
    '''
    A regular school grade to be used in student profiles.
    '''
    pass
    # name
