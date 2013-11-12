from django.contrib             import admin
from django                     import forms
from django.db.models           import fields
from dragon_portal.models       import Course, DragonUser, ParentProfile, \
                                       Progress, StudentProfile
from django.contrib.auth.admin  import UserAdmin
from django.contrib.auth.forms  import UserChangeForm, UserCreationForm
from django.contrib.admin.views.main import ChangeList

from dragon_portal              import forms as ddforms



############
## Mixins ##
############

class UserNamesMixin(object):
    '''
    User profiles don't directly have standard user fields. This mixin class
    adds a read-only reference to those fields.
    '''
    list_display      = ('username', 'first_name', 'last_name', 'email', )
    actions_on_top    = True
    actions_on_bottom = True
    save_on_top       = True

    def username(self, obj):
        return obj.dragonuser.username
    def first_name(self, obj):
        return obj.dragonuser.first_name
    def last_name(self, obj):
        return obj.dragonuser.last_name
    def email(self, obj):
        return obj.dragonuser.email

    def get_users(self):
        return self.dragonuser

    username.short_description   = 'Username'
    first_name.short_description = 'First name'
    last_name.short_description  = 'Last name'
    email.short_description      = 'Email address'

class ParentMixin(object):
    '''
    This mixin class adds a read-only reference to a student's parent name.
    '''
    def parent(self, obj):
        return obj.parent.dragon_user.full_name

    parent.short_description = 'Parent'


####################
## Inline classes ##
####################

class ProgressInline(admin.TabularInline):
    model = Progress
    extra = 0

class DragonUserInline(admin.StackedInline):
    model  = DragonUser
    extra  = 1
    fields = ('username', 'password', 'first_name', 'last_name', 'email')


# A reference to students doen't have the same name when referred to from
# classes or from parent profiles. So this class is used through its
# subclasses that each have the right set of verbose names.
class StudentInline(admin.TabularInline, UserNamesMixin):
    model   = StudentProfile
    extra   = 0
    fields  = ('username', 'first_name', 'last_name', 'email')
    readonly_fields = fields

class ChildrenInline(StudentInline):
    verbose_name        = 'Related student'
    verbose_name_plural = 'Related students'

class EnrolledInline(StudentInline):
    verbose_name        = 'Enrolled student'
    verbose_name_plural = 'Enrolled students'

class CourseInline(admin.StackedInline):
    model   = Course
    extra   = 3

class ParentInline(admin.TabularInline, UserNamesMixin):
    model   = ParentProfile
    maxnum  = 1
    extra   = 1
    fields  = ('username', 'first_name', 'last_name', 'email')
    readonly_fields = fields


class DragonUserAdmin(UserAdmin):
    add_form_template = 'dragon_portal/add_admin.html'
    save_on_top       = True


###################
## Admin classes ##
###################

class BaseUserAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        defaults = {}
        if obj is None:
            defaults.update({
                'form': self.add_form,
            })
        defaults.update(kwargs)
        return super(BaseUserAdmin, self).get_form(request, obj, **defaults)
    def get_changelist(self, request, **kwargs):
        return super(BaseUserAdmin, self).get_changelist(request, **kwargs)

class StudentAdmin(BaseUserAdmin, UserNamesMixin, ParentMixin):
    list_display = UserNamesMixin.list_display + ('parent',)
    add_form     = ddforms.StudentCreationForm
    form         = ddforms.StudentChangeForm
#    inlines    = (CourseInline,)

class ParentAdmin(BaseUserAdmin, UserNamesMixin):
    list_display = UserNamesMixin.list_display
    add_form     = ddforms.ParentCreationForm
    form         = ddforms.ParentChangeForm
    inlines      = (ChildrenInline,)


class CourseAdmin(admin.ModelAdmin):
    inlines = (ProgressInline,)


##################
## Registration ##
##################

admin.site.register(Course,         CourseAdmin    )
admin.site.register(DragonUser,     DragonUserAdmin)
admin.site.register(ParentProfile,  ParentAdmin    )
admin.site.register(StudentProfile, StudentAdmin   )