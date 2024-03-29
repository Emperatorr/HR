from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager
import datetime
import django

class SentMail(models.Model):
    full_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100)
    title = models.CharField(max_length=150, null=True)
    message = models.TextField(null=True)
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

## Les choix 
GENRE_CHOICES = (
    ('man', _('man')),
    ('woman', _('woman'))
)

CATEGORIE_CHOICES = (
    ('employe', _('Employe')),
    ('manager', _('Manager'))
)

class User(AbstractBaseUser, PermissionsMixin):
    ''' the user for public worker and admins ... '''
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['email', 'last_name']

    class Meta:
        abstract = True
        ordering = ('id',)
        verbose_name = 'User'
        verbose_name_plural = 'Users'

# les fonctions
class Fonction(models.Model):
    name = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return '{}'.format(self.name)

# Departements
class Departement(models.Model):
    name = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.name)

# Type conges
class Type_conge(models.Model):
    name = models.CharField(max_length=100, null=True)
    indice = models.FloatField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.name)

class Employe(User):
    matricule = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=40, default='')
    last_name = models.CharField(max_length=40, default='', null=True)
    fonction = models.ForeignKey(Fonction, related_name='fonctions')
    departement = models.ForeignKey(Departement, related_name='departements')
    is_manager = models.BooleanField(default=False, blank=True)
    id_manager = models.CharField(max_length=100, blank=True, null=True)
    phone1 = models.CharField(max_length=50, null=True)
    phone2 = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=100, null=True)
    genre = models.CharField(max_length=100, blank=True, choices=GENRE_CHOICES, default='')

    def __str__(self):
        return '{}'.format(self.first_name)

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)
        
    def get_short_name(self):
        return self.first_name

# Stock des conges
class Conge(models.Model):
    employe = models.ForeignKey(Employe, related_name='employe')
    type_conge = models.ForeignKey(Type_conge, related_name='conges')
    nombre_jour = models.IntegerField(default=0)
    last_calculation_date = models.DateTimeField(auto_now_add=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Demande des conges
class Demande(models.Model):
    employe = models.ForeignKey(Employe, related_name='employes')
    type_conge = models.ForeignKey(Type_conge, related_name='type_conges')
    nombre_jour = models.IntegerField(default=1)
    status = models.IntegerField(default=0)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    reason = models.TextField(null=True)
    by = models.ForeignKey(Employe, related_name='reviewer', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Document(models.Model):
    employe = models.ForeignKey(Employe, related_name='documents')
    type_document = models.FileField(upload_to='', default='')
    document = models.FileField(upload_to='', default='')
    document_uploaded_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
