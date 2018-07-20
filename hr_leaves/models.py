from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django_countries import countries
from django_countries.fields import CountryField
from .managers import UserManager
from django import utils
import datetime
import django

from django.contrib.contenttypes.fields import GenericRelation

class SentMail(models.Model):
    full_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100)
    title = models.CharField(max_length=150, null=True)
    message = models.TextField(null=True)
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

GENRE_CHOICES = (
    ('man', _('man')),
    ('woman', _('woman'))
)

class User(AbstractBaseUser, PermissionsMixin):
    ''' the user for public worker and admins ... '''
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=40, default='')
    last_name = models.CharField(max_length=40, default='', null=True)
    id_number = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=250, default='')
    phone = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=100, null=True)
    matricule = models.CharField(max_length=100, blank=True, null=True)
    genre = models.CharField(max_length=100, blank=True, choices=GENRE_CHOICES, default='')

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        ordering = ('id',)
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return '{}'.format(self.first_name)

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse('user_profile', args=[self.id])