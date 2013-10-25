from django.contrib             import admin
from dd_portal.models           import Course, Student, Parent
from django.contrib.auth.models import User
from django.contrib.auth.admin  import UserAdmin

admin.site.register(Course)
admin.site.register(Student, UserAdmin)
admin.site.register(Parent, UserAdmin)