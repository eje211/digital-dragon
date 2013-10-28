from django.contrib             import admin
from django                     import forms
from dragon_portal.models       import Course, DragonUser, ParentProfile, Progress, StudentProfile
from django.contrib.auth.admin  import UserAdmin
from django.contrib.auth.forms  import UserChangeForm, UserCreationForm

class ProgressInline(admin.TabularInline):
    model = Progress
    extra = 0

class DragonUserCreationForm(UserCreationForm):
    '''
    '''
    def __init__(self, *args, **kwargs):
        print("Doin' stuff...")
        from pprint import pprint
        pprint(dir(self))
        pprint(self.base_fields)
        return UserCreationForm.__init__(self, *args, **kwargs)

    class Meta:
        model  = DragonUser
        fields = ()

class DragonUserAdmin(UserAdmin):
    add_form_template = 'dragon_portal/add_admin.html'
    save_on_top       = True


# class ParentProfileInline(admin.StackedInline):
#     model = ParentProfile
# 
# class ParentChangeForm(UserChangeForm):
#     '''
#     For the admin version of the parent edit form, we'll just use 
#     '''
#     class Meta(UserChangeForm.Meta):
#         model = Parent
# 
# class ParentAdmin(UserAdmin):
#     add_form    = ParentCreationForm
#     form        = ParentChangeForm
#     save_on_top = True
# 
#     def get_inline_instances(self, request, obj = None):
#         if request.path.split('/')[-2] != 'add':
#             self.inlines = (ProgressInline,)
#         return super(UserAdmin, self).get_inline_instances(request, obj)
# 
# 
# 
# class StudentCreationForm(UserCreationForm):
#     '''
#     For the admin version of the parent edit form, we'll just use 
#     '''
#     parent = forms.ModelChoiceField(queryset = Parent.objects.all())
# 
#     class Meta(UserCreationForm.Meta):
#         model  = Student
#         fields = ("parent",)
# 
# class StudentChangeForm(UserChangeForm):
#     '''
#     For the admin version of the parent edit form, we'll just use 
#     '''
#     class Meta(UserChangeForm.Meta):
#         model = Student
# 
# class StudentAdmin(UserAdmin):
#     add_form     = StudentCreationForm
#     form         = StudentChangeForm
#     save_on_top  = True
#     list_display = ('last_name', 'first_name', 'username', 'email')
# #     inlines      = (StudentProfile,)
#     fieldsets    = UserAdmin.fieldsets[:2] + (
#             ('Student details', {
#                 'fields': ('parent',)
#             }),
#         ) + UserAdmin.fieldsets[2:]
# 
# #     def get_inline_instances(self, request, obj = None):
# #         if request.path.split('/')[-2] != 'add':
# #             self.inlines = (ProgressInline,)
# #         return super(UserAdmin, self).get_inline_instances(request, obj)
# # 
# #     def get_fieldsets(self, request, obj=None):
# #         if request.path.split('/')[-2] != 'add':
# #             self.fieldsets = fieldsets[:2] + (
# #             ('Student details', {
# #                 'fields': ('parent', 'school_grade')
# #             }),
# #         ) + fieldsets[2:]
# #         return super(UserAdmin, self).get_fieldsets(request, obj)
# 
class CourseAdmin(admin.ModelAdmin):
    inlines = (ProgressInline,)

# 
# 
admin.site.register(Course,     CourseAdmin    )
admin.site.register(DragonUser, DragonUserAdmin)
# admin.site.register(Student, StudentAdmin)
# admin.site.register(Parent,  ParentAdmin )