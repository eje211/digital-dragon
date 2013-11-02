from django                    import forms
from django.utils.translation  import ugettext, ugettext_lazy as _
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from dragon_portal.models      import DragonUser, ParentProfile, StudentProfile
from django.forms.models       import fields_for_model, model_to_dict
from tinymce.models            import HTMLField


#
# TODO:
#   * Add emergency contact validation to the parent profile.
#   * Make creation forms.
#

class PersonForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }

    first_name  = forms.CharField(max_length=100)
    last_name   = forms.CharField(max_length=100)
    email       = forms.EmailField()

    class Meta:
        exclude = ('dragonuser',)
        fields  = ('username', 'password1', 'password2', 'first_name', 
            'last_name', 'email')

    def __init__(self, *args, **kwargs):
        '''
        Based on <http://stackoverflow.com/questions/15889794/creating-one-django-form-to-save-two-models>.
        Merge the fields from the actual user (DragonUser) and the user
        profile (ParentProfile) and present them as a whole on the interface.
        '''
        try: instance = kwargs['instance']
        except KeyError: instance = None
        # The fields we want to add to ParentProfile.
        _fields = ('username', 'first_name',
            'last_name', 'email', )
        # Get the current values of the DragonUser fields.
        _initial = model_to_dict(instance.dragonuser, _fields) \
            if instance is not None else {}
        kwargs['initial'] = _initial
        # Actually initialize the class.
        super(PersonForm, self).__init__(*args, **kwargs)
        # From the StackOverflow code, but not needed here.
        # self.fields.update(fields_for_model(DragonUser, _fields))
        self.fields.update(fields_for_model(DragonUser, _fields))
        # Override the class attribute for the input widgets:
        for field in _fields + ('password1', 'password2'):
            self.fields[field].widget.attrs['class'] = 'vTextField'

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if self.CHANGEFORM and password1 == password2 == '':
            return password2
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'])
        return password2

    def save_user(self):
        # Get the instance of the user and save the values present on the
        # current form.
        u            = self.instance.dragonuser
        if u == None: raise(Exception(
            'The parent profile %s is not linked to a valid user.' % self.id))
        u.first_name = self.cleaned_data['first_name']
        u.last_name  = self.cleaned_data['last_name']
        u.email      = self.cleaned_data['email']
        # Only save password if it's not blank:
        if self.cleaned_data["password1"] != '':
            u.set_password(self.cleaned_data["password1"])
        u.save()

    def save(self, *args, **kwargs):
        # First, save the current user data:
        self.save_user()
        # Then, automatically process the current model.
        profile = super(PersonForm, self).save(*args, **kwargs)
        return profile


class ParentFormMixin(object):
    class Meta(PersonForm.Meta):
        model  = ParentProfile
        fields = PersonForm.Meta.fields + ('ice_contact', 'notes')

class StudentFormMixin(object):
    class Meta(PersonForm.Meta  ):
        model  = StudentProfile
        fields = PersonForm.Meta.fields + ('school_grade', 'parent')

class ChangeForm(PersonForm):
    CHANGEFORM = True
    username   = forms.CharField()
    password1  = forms.CharField(label=_("Password"), required=False,
        widget=forms.PasswordInput,
        help_text= _("Enter a new password and confirm to change it, or leave "
            "both fields blank to keep it unchanged."))
    password2  = forms.CharField(label=_("Password (again)"), required=False,
                                widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        super(ChangeForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        # Overrite some of the default properties of the "username" field.
        self.fields['username'].help_text = ''


class CreationForm(PersonForm):
    '''
    The Parent Creation Form is the same as the Parent Change Form except
    the interface has different password fields. Also, the parent creation
    needs to handle a user creation.
    '''
    CHANGEFORM = False
    username   = forms.RegexField(
        label=_("Username"), max_length=30, regex=r"^[\w.@+-]+$",
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                      "@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")})
    password1  = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput,
        help_text=_("Enter a password.")
    )
    password2  = forms.CharField(label=_("Password (again)"),
        widget=forms.PasswordInput,
        help_text=_("And enter it again for confirmation.")
    )

class ParentChangeForm   (ParentFormMixin,  ChangeForm  ): pass

class ParentCreationForm (ParentFormMixin,  CreationForm): pass

class StudentChangeForm  (StudentFormMixin, ChangeForm  ): pass

class StudentCreationForm(StudentFormMixin, CreationForm): pass
