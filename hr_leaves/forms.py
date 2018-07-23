from django import forms
from django.forms.widgets import DateTimeInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import *
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from hr_leaves.models import *
import datetime
from django.forms.extras.widgets import SelectDateWidget

CATEGORIE_CHOICES = (
    ('employe', _('Employe')),
    ('manager', _('Manager'))
)

class RegistrationForm(UserCreationForm):

    class Meta:
        model = Employe
        fields = ('email', 'first_name', 'last_name', 'password1',
                  'password2', 'matricule', 'genre')
        labels = {
            'matricule': _('Matricule'),
            'email': _('Email'),
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
            'departement': _('Departement'),
            'genre': _('Genre')
        }

    def __init__(self, user_obj, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'matricule',
            'first_name',
            'last_name',
            'genre',
            'email',
            'password1',
            'password2',
            'departement',
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

class DepartementForm(forms.ModelForm):
     class Meta:
        model = Departement
        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Department name',
                'class': 'form-control'
            })
        }

class FonctionForm(forms.ModelForm):
    class Meta:
        model = Fonction
        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Function name',
                'class': 'form-control'
            })
        }
        
class DemandeForm(forms.ModelForm):

    class Meta:
        model = Demande
        fields = ('type_conge', 'nombre_jour', 'date_debut', 'date_fin', 'reason')
        widgets = {
            'type_conge': forms.Select(attrs={
                'placeholder': _('Type'),
                'class': 'form-control'
            }),
            'nombre_jour': forms.fields.TextInput(attrs={
                'placeholder': _('Nomber of day'),
                'class': 'form-control',
                'type': 'number',
                'required': 'True',
                'title' : _('A integer > 0')
            }),
             'date_debut': forms.fields.DateInput(attrs={
                'type': 'date',
                'class': 'form-date',
                'required': 'true'
            }),
            'date_fin': forms.fields.DateInput(attrs={
                'type': 'date',
                'class': 'form-date',
                'required': 'true'
            }),
            'reason': forms.Textarea(attrs={
                'placeholder': _('Reason'),
                'class': 'form-control',
                'required': 'True',
                'cols': '40',
                'rows': '4',
                'title' : _('Reason')
            })
        }
class EmployeForm(forms.ModelForm):

    class Meta:
        model = Employe
        fields = ('matricule', 'first_name', 'last_name', 'phone1', 'phone2', 'address', 'email' )

        exclude = ('is_manager', 'id_manager')

        widgets = {
            'matricule': forms.fields.TextInput(attrs={
                'placeholder': 'Le matricule de l\'employé',
                'class': 'form-control'
            }),
            'first_name': forms.fields.TextInput(attrs={
                'placeholder': 'Le prénom de l\'employé',
                'class': 'form-control'
            }),
            'last_name': forms.fields.TextInput(attrs={
                'placeholder': 'Le nom de l\'employé',
                'class': 'form-control'
            }),
            'email': forms.fields.EmailInput(attrs={
                'placeholder': 'Adresse email',
                'class': 'form-control'
            }),
            'phone1': forms.fields.TextInput(attrs={
                'placeholder': 'Numero de telephone',
                'class': 'form-control',
                'type': 'tel',
                'id' : 'phone',
                'min' : '600000000',
                'max' : '699999999',
                'pattern' : '^6(3|2|6|5)[0-9]{7}',
                'title' : 'S\'il vous plait veuiller respecter le format de telephone guineen'
            }),
            'phone2': forms.fields.TextInput(attrs={
                'placeholder': 'Numero de telephone',
                'class': 'form-control',
                'type': 'tel',
                'id' : 'phone',
                'min' : '600000000',
                'max' : '699999999',
                'required': 'False',
                'pattern' : '^6(3|2|6|5)[0-9]{7}',
                'title' : 'S\'il vous plait veuiller respecter le format de telephone guineen'
            }),
            'address': forms.Textarea(attrs={
                'placeholder': 'Adresse',
                'class': 'form-control',
                'cols': '10',
                'row': '5'
            }),
            
        }

    CHOICES = (
        ("Masculin", _("Masculin")),
        ("Feminin", _("Feminin"))
    )

    genre = forms.ChoiceField(choices = CHOICES, label="Genre", initial='', widget=forms.Select(attrs={'class':'form-control'}), required=True)

    departement = forms.ModelChoiceField(
                    queryset=Departement.objects.all(),
                    widget=forms.Select(attrs={'class':'form-control'})
                    )

    fonction = forms.ModelChoiceField(
                    queryset=Fonction.objects.all(),
                    widget=forms.Select(attrs={'class':'form-control'})
                    )

class UpdateEmployForm(forms.ModelForm):
    def __init__(self, matricule, first_name, last_name, fonction, departement, phone1, phone2, address, email, genre, * args, **kwargs):
        super(UpdateEmployForm, self).__init__(*args, **kwargs)
        
        self.initial['matricule']     = matricule
        self.initial['first_name']     = first_name
        self.initial['last_name']     = last_name
        self.initial['fonction']     = fonction
        self.initial['departement']     = departement
        self.initial['phone1']     = phone1
        self.initial['phone2']     = phone2
        self.initial['address']     = address
        self.initial['email']     = email
        self.initial['genre'] = genre

    class Meta:
        model   = Employe
        fields  = ['matricule','first_name','last_name', 'fonction', 'departement', 'phone1', 'phone2', 'address', 'email', 'genre']

        widgets = {
                'matricule': forms.TextInput(attrs={
                    'placeholder': 'Matricule',
                    'class': 'form-control'
                }),
                'first_name': forms.TextInput(attrs={
                    'placeholder': 'Prenom',
                    'class': 'form-control'
                }),
                'last_name': forms.TextInput(attrs={
                    'placeholder': 'Nom',
                    'class': 'form-control'
                }),
                'fonction': forms.Select(attrs={
                    'placeholder': 'fonction',
                    'class': 'form-control'
                }),
                'departement': forms.Select(attrs={
                    'placeholder': 'Departement',
                    'class': 'form-control'
                }),
                'phone1': forms.fields.TextInput(attrs={
                    'placeholder': 'Numero de telephone',
                    'class': 'form-control',
                    'type': 'tel',
                    'id' : 'phone',
                    'min' : '600000000',
                    'max' : '699999999',
                    'pattern' : '^6(3|2|6|5)[0-9]{7}',
                    'title' : 'S\'il vous plait veuiller respecter le format de telephone guineen'
                }),
                'phone2': forms.fields.TextInput(attrs={
                    'placeholder': 'Numero de telephone',
                    'class': 'form-control',
                    'type': 'tel',
                    'id' : 'phone',
                    'min' : '600000000',
                    'max' : '699999999',
                    'pattern' : '^6(3|2|6|5)[0-9]{7}',
                    'title' : 'S\'il vous plait veuiller respecter le format de telephone guineen'
                }),
                'address': forms.Textarea(attrs={
                    'placeholder': 'Adresse',
                    'class': 'form-control',
                    'cols': '10',
                    'row': '5'
                }),
                'email': forms.fields.EmailInput(attrs={
                    'placeholder': 'Adresse email',
                    'class': 'form-control'
                }),
                'genre': forms.Select(attrs={
                    'placeholder': 'Genre',
                    'class': 'form-control'
                }),
            }
        

