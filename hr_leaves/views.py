import os
import json
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse, Http404
from django.conf import settings
from django.forms import formset_factory
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.mail import send_mail, EmailMessage
from django.core.exceptions import ImproperlyConfigured
from django.views import generic
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from .forms import *
from .models import *
from rest_framework import generics
from . import serializers
from .chart_data import *

import datetime
from django.utils.formats import localize
from django.template.loader import render_to_string
from django.utils.dateparse import parse_datetime
from chartit import DataPool, Chart
from django.shortcuts import render_to_response

from django.contrib.auth.hashers import make_password
from math import *

class RegistrationView(generic.CreateView):
    form_class = RegistrationForm
    form_valid_message = _('you have successfully signed up')
    success_url = reverse_lazy('login')
    model = Employe
    template_name = 'hr_leaves/register.html'



class LoginView(generic.FormView):
    form_class = LoginForm
    form_valid_message = 'you are logged in'
    model = Employe
    success_url = reverse_lazy('acceuil')
    template_name = 'hr_leaves/login.html'

    def get_success_url(self):
        """
        Returns the supplied URL.
        """
        if self.success_url:
            self.request.user.is_agency = False
            url = reverse('acceuil')
        else:
            try:
                url = self.object.get_absolute_url()
            except AttributeError:
                raise ImproperlyConfigured(
                    "No URL to redirect to.  Either provide a url or define"
                    " a get_absolute_url method on the Model."
                )
        return url

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return super().form_valid(locals())
        else:
            return self.form_invalid(locals())


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def delete_user(request, user_id):
    user = Employe.objects.get(id=user_id)

    context = {'user': user.get_full_name()}
    html_content = render_to_string('mails/user_account_delete.html', context)

    # mail = SentMail()
    # mail.full_name = request.user.get_full_name()
    # mail.title = _('Account Deleted')
    # mail.email = user.email
    # mail.message = html_content
    # mail.save()

    user.delete()
    messages.success(request, _('Account succesfully deleted'))
    return redirect('users')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            messages.success(request, _('Your password was Successfully Updated!'))
            return redirect('acceuil')
        else:
            messages.error(request, _('Please correct the errors below!'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'hr_leaves/change_password.html', {
        'form': form
        })

@login_required
def user_profile(request, user_id):
    user = Employe.objects.get(id=user_id)
    fonctions = Fonction.objects.all()
    departments = Departement.objects.all()

    return render(request, 'hr_leaves/user_profile.html', {'users': user, 'departments': departments, 'fonctions': fonctions, 'genders': GENRE_CHOICES})

@login_required
def update_user_profile(request, user_id):
    if request.method == 'POST':
        user = Employe.objects.get(id=user_id)

        user.email = request.POST.get('email', None)
        user.first_name = request.POST.get('first_name', None)
        user.last_name = request.POST.get('last_name', None)
        user.phone1 = request.POST.get('phone1', '')
        user.phone2 = request.POST.get('phone2', '')
        user.address = request.POST.get('address', None)
        user.genre = request.POST.get('gender', None)

        user.save()
        messages.success(request, _('Your Profil has been updated succesfully'))
        return redirect('acceuil')

        user.save()

    else:
        return redirect('user_profile', user.id)

@login_required
def user_account(request, user_id):
    company = User.objects.get(id=user_id)
    missions = Mission.objects.all()

    return render(request, 'hr_leaves/user_account.html', {
        'user': company,
        'missions': missions
    })

def get_client_ip(request):
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        elif request.META.get('HTTP_X_REAL_IP'):
            ip = request.META.get('HTTP_X_REAL_IP')
        else:
            ip = request.META.get('REMOTE_ADDR')
    except:
        ip = ""
    return ip

def create_success(request):
    return render(request, 'hr_leaves/create_success.html',)
    

@login_required
def delete_user(request, user_id):
    user = Employe.objects.get(id=user_id)
    user.delete()
    messages.success(request, _('Account succesfully deleted'))
    return redirect('users')


@login_required
def acceuil(request):
    return render(request, 'hr_leaves/acceuil.html',)