from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User)
    # parent
    # classes
    # grade

class Parent(models.Model):
    user = models.OneToOneField(User)
    # student

class Course(model.Model):
    pass
    # name
    # description
    # students

