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
def demande(request):
    form = DemandeForm()
    if request.method == 'POST':
        form = DemandeForm(request.POST)
        if form.is_valid():
            
            type_conge = form.cleaned_data['type_conge']
            nombre_jour = form.cleaned_data['nombre_jour']
            date_debut = form.cleaned_data['date_debut']
            date_fin = form.cleaned_data['date_fin']

            print('type: ' + str(type_conge))
            print('nombre: ' + str(nombre_jour))
            print('date_debut: ' + str(date_debut))
            print('date_fin : ' + str(date_fin))

            demande = Demande()
            demande.type_conge = type_conge
            demande.nombre_jour = nombre_jour
            demande.date_debut = date_debut
            demande.date_fin = date_fin
            demande.employe = request.user
            demande.save()

            messages.success(request, _('Your request is successfuly sent'))
            return redirect('all_demande')
        else:
            messages.error(request, _('Please correct the errors below!'))
    return render(request, 'hr_leaves/demande.html', {'form': form })

@login_required
def all_demande(request):
    demandes = Demande.objects.filter(employe=request.user)
    return render(request, 
    'hr_leaves/all_demande.html', {'demandes': demandes })

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
def register(request):
    form = EmployeForm()

    if request.method == 'POST':
        form = EmployeForm(request.POST)
        typ_conge = Type_conge.objects.all()

        if form.is_valid():
            empoly = Employe()
            

            empoly.matricule = form.cleaned_data['matricule']
            empoly.first_name = form.cleaned_data['first_name']
            empoly.last_name = form.cleaned_data['last_name']
            empoly.email = form.cleaned_data['email']
            empoly.genre = form.cleaned_data['genre']
            empoly.fonction = form.cleaned_data['fonction']
            empoly.departement = form.cleaned_data['departement']
            empoly.phone1 = form.cleaned_data['phone1']
            empoly.phone2 = form.cleaned_data['phone2']
            empoly.address = form.cleaned_data['address']

            empoly.save()

            for typ in Type_conge.objects.all():

                conge = Conge()
                
                conge.employe = Employe.objects.last()
                conge.type_conge = typ
                conge.nombre_jour = 0
                print(typ.indice)
                conge.save()
                print("end save")


            


            messages.success(request, 'Vous avez bien ajouté un employé')
            return redirect('employees')
            

        else:
            print("not valid")

    return render(request, 'hr_leaves/register.html', {'form':form})

@login_required
def list_employ(request):
    all_user = Employe.objects.all()

    return render(request, 'hr_leaves/users.html', {'all_user':all_user})

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