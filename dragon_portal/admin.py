from django.contrib             import admin
from django                     import forms
from dragon_portal.models       import Course, DragonUser, ParentProfile, \
                                       Progress, StudentProfile
from django.contrib.auth.admin  import UserAdmin
from django.contrib.auth.forms  import UserChangeForm, UserCreationForm


class UserNamesMixin(object):
    def username(self, obj):
        return obj.dragonuser.username
    def first_name(self, obj):
        return obj.dragonuser.first_name
    def last_name(self, obj):
        return obj.dragonuser.last_name
    def email(self, obj):
        return obj.dragonuser.email

    username.short_description   = 'Username'
    first_name.short_description = 'First name'
    last_name.short_description  = 'Last name'
    email.short_description      = 'Email address'

class ParentMixin(object):
    def parent(self, obj):
        return obj.parent.dragon_user.full_name

    parent.short_description = 'Parent'


class ProgressInline(admin.TabularInline):
    model = Progress
    extra = 0

class DragonUserInline(admin.StackedInline):
    model  = DragonUser
    extra  = 1
    fields = ('username', 'password', 'first_name', 'last_name', 'email')

class StudentInline(admin.TabularInline, UserNamesMixin):
    model   = StudentProfile
    extra   = 0
    fields  = ('username', 'first_name', 'last_name', 'email')
    readonly_fields = fields

class ParentInline(admin.TabularInline, UserNamesMixin):
    model   = ParentProfile
    maxnum  = 1
    extra   = 1
    fields  = ('username', 'first_name', 'last_name', 'email')
    readonly_fields = fields


class DragonUserAdmin(UserAdmin):
    add_form_template = 'dragon_portal/add_admin.html'
    save_on_top       = True


class PersonAdmin(admin.ModelAdmin, UserNamesMixin, ParentMixin):
    add_form_template    = 'dragon_portal/change_form.html'
    change_form_template = add_form_template
    list_view            = ('username', 'first_name', 'last_name', 'email')
    inlines              = (DragonUserInline,)
    actions_on_top       = True
    actions_on_bottom    = True
    save_on_top          = True

class StudentAdmin(PersonAdmin):
    list_view = PersonAdmin.list_view + ('parent',)

class ParentAdmin(PersonAdmin):
    inlines = PersonAdmin.inlines + (StudentInline,)


class CourseAdmin(admin.ModelAdmin):
    inlines = (ProgressInline,)


admin.site.register(Course,         CourseAdmin    )
admin.site.register(DragonUser,     DragonUserAdmin)
admin.site.register(ParentProfile,  ParentAdmin    )
admin.site.register(StudentProfile, StudentAdmin   )