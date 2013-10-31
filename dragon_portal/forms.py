from django                    import forms
from django.utils.translation  import ugettext, ugettext_lazy as _
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from dragon_portal.models      import DragonUser, ParentProfile, StudentProfile
from django.forms.models       import fields_for_model, model_to_dict
from tinymce.models            import HTMLField


class ParentChangeForm(forms.ModelForm):
    username    = forms.CharField()
    # The "username" field is customized in the __init__ function below.
    first_name  = forms.CharField(max_length=100)
    last_name   = forms.CharField(max_length=100)
    email       = forms.EmailField()

    class Meta:
        model   = ParentProfile
        exclude = ('dragonuser',)
        fields  = ('username', 'first_name', 'last_name', 'email',
            'ice_contact', 'notes')

    def __init__(self, *args, **kwargs):
        '''
        Based on <http://stackoverflow.com/questions/15889794/creating-one-django-form-to-save-two-models>.
        Merge the fields from the actual user (DragonUser) and the user
        profile (ParentProfile) and present them as a whole on the interface.
        '''
        try: instance = kwargs['instance']
        except KeyError: instance = None
        # The fields we want to add to ParentProfile.
        _fields = ('username', 'first_name', 'last_name', 'email')
        # Get the current values of the DragonUser fields.
        _initial = model_to_dict(instance.dragonuser, _fields) \
            if instance is not None else {}
        kwargs['initial'] = _initial
        # Actually initialize the class.
        super(ParentChangeForm, self).__init__(*args, **kwargs)
        # From the StackOverflow code, but not needed here.
        # self.fields.update(fields_for_model(DragonUser, _fields))
        self.fields.update(fields_for_model(DragonUser, _fields))
        # Overrite some of the default properties of the "username" field.
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['username'].help_text = (
          "Raw passwords are not stored, so there is no way to see "
          "this user's password, but you can change the password "
          "using <a href=\"password/\">this form</a>.")

    def save_user(self):
        # Get the instance of the user and save the values present on the
        # current form.
        u            = self.instance.dragonuser
        u.first_name = self.cleaned_data['first_name']
        u.last_name  = self.cleaned_data['last_name']
        u.email      = self.cleaned_data['email']
        u.save()

    def save(self, *args, **kwargs):
        # First, save the current user data:
        self.save_user()
        # Then, automatically process the current model.
        profile = super(ParentCreationForm, self).save(*args, **kwargs)
        return profile


class ParentCreationForm(ParentChangeForm):
    '''
    The Parent Creation Form is the same as the Parent Change Form except interface
    has a password creation field right on the form.
    '''
    pass