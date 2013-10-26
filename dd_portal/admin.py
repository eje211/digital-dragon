from django.contrib             import admin
from dd_portal.models           import Course, Parent, Progress, Student
from django.contrib.auth.models import User
from django.contrib.auth.admin  import UserAdmin
from django.contrib.auth.forms  import UserChangeForm, UserCreationForm
from django.http                import HttpRequest 

class ProgressInline(admin.TabularInline):
    model = Progress
    extra = 0


class ParentChangeForm(UserChangeForm):
    '''
    For the admin version of the parent edit form, we'll just use 
    '''
    class Meta(UserChangeForm.Meta):
        model = Parent

class ParentAdmin(UserAdmin):
    add_form     = UserCreationForm
    form         = ParentChangeForm
    save_on_top  = True
    list_display = ('last_name', 'first_name', 'username', 'email')

    def get_fieldsets(self, request):
        if request.path.split('/')[-2] == 'add':
            return UserAdmin.fieldsets
        return UserAdmin.fieldsets[:2] + (
            ('Parent details', {
                'fields': ('ice_contact', 'notes')
            }),
        ) + UserAdmin.fieldsets[2:]


class StudentChangeForm(UserChangeForm):
    '''
    For the admin version of the parent edit form, we'll just use 
    '''
    class Meta(UserChangeForm.Meta):
        model = Student

class StudentAdmin(UserAdmin):
    add_form     = UserCreationForm
    form         = StudentChangeForm
    save_on_top  = True
    list_display = ('last_name', 'first_name', 'username', 'email')
 
#     def get_inline_instances(self, request, obj = None):
#         if request.path.split('/')[-2] == 'add':
#             return (ProgressInline,)
#         return ()

    def get_fieldsets(self, request, obj = None):
        fieldsets = super(UserAdmin, self).get_fieldsets(request, obj)
        return fieldsets
#         if request.path.split('/')[-2] == 'add':
#             return fieldsets
#         return fieldsets[:2] + (
#             ('Student details', {
#                 'fields': ('parent', 'school_grade')
#             }),
#         ) + fieldsets[2:]

class CourseAdmin(admin.ModelAdmin):
    inlines = (ProgressInline,)



admin.site.register(Course, CourseAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Parent,  ParentAdmin)