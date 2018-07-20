from django.conf.urls import url, include
from .views import (
    LoginView,
    RegistrationView,
    logout_view,
    user_profile,
    update_user_profile,
    change_password,
    create_success,
    delete_user,
    demande,
    all_demande,
    acceuil
    )

urlpatterns = [
    url(r'^$', LoginView.as_view(), name='login'),
    url(r'^enregistrement/$', RegistrationView.as_view(), name='register'),
    url(r'^deconnection/$', logout_view, name='logout'),
    url(r'^mon-profile/(?P<user_id>[0-9]+)/$', user_profile, name='user_profile'),
    url(r'^mise-a-jour-des-informations-de-l-utilisateur/(?P<user_id>[0-9]+)$', update_user_profile, name='update_user'),
    url(r'^suppression-de-l-utilisateur/(?P<user_id>[0-9]+)$', delete_user, name='delete_user'),
    url(r'^changement-de-mot-de-passe/$', change_password, name='change_password'),
    url(r'^creation-avec-success/$', create_success, name='create_success'),
    url(r'^creation-demande/$', demande, name='leave_request'),
    url(r'^all-demande/$', all_demande, name='all_demande'),
    url(r'^acceuil/$', acceuil, name='acceuil'),
    
]
