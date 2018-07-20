from django import forms
from django.forms.widgets import DateTimeInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import *
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from hr_leaves.models import User
import datetime
from django.forms.extras.widgets import SelectDateWidget

class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1',
                  'password2', 'id_number', 'position', 'matricule', 'genre')
        labels = {
            'matricule': _('Matricule'),
            'email': _('Email'),
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
            'id_number': _('ID Number'),
            'position': _('Position'),
            'departement': _('Departement'),
            'genre': _('Genre')
        }

    def __init__(self, user_obj, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'etat',
            'matricule',
            'first_name',
            'last_name',
            'genre',
            'email',
            'password1',
            'password2',
            'id_number',
            'position',
            'departement',
            'ministry',
            ButtonHolder(
                Submit('register', _('Register'))
            )
        )

        if user_obj.is_controller:
            self.initial['ministry'] = user_obj.ministry.id
            self.fields['ministry'].disabled = True


class LoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ('email', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                _('Login'),
                Field('username', id="username-field", placeholder=_("Your email address")),
                Field('password', id="password-field", placeholder=_("Your password"))
            ),
            ButtonHolder(
                Submit('login', _('Log in'))
            )
        )