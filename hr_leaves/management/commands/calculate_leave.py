from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail, EmailMessage
from config import settings
from hr_leaves.models import Conge, Type_conge
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
import datetime
import logging

class Command(BaseCommand):
    help = 'Calculating email'

    def handle(self, *args, **options):
        
        self.stdout.write('executing....')
        #try:
        calculate_leaves()
        #except Exception as e: print('error message while sending email')
        self.stdout.write('everything is ok')


def calculate_leaves():
    conges = Conge.objects.all()
    for conge in conges:
        if conge.last_calculation_date is not None:
            
            interval = get_interval_from_date_to_now(conge.last_calculation_date)
            interval_day = interval.days
            month_days = 30
            indice = Type_conge.objects.get(id=conge.type_conge.id).indice
            
            while ((interval_day - month_days) >= 1):
                conge.nombre_jour = (float(conge.nombre_jour) + float(indice))
                # print('nouveau nbre jours : ' + str(conge.nombre_jour))
                
                interval_day -= month_days
                conge.last_calculation_date = datetime.datetime.now()
                conge.save()

# calculate the interval from a giving date to now
def get_interval_from_date_to_now(old_date):
    dateyear = old_date.year
    datemonth = old_date.month
    dateday = old_date.day
    datehour = old_date.hour
    dateminute = old_date.minute
    datesecond = old_date.second
    datemicrosecond = old_date.microsecond

    interval = datetime.datetime.now() - datetime.datetime(dateyear, datemonth, dateday, datehour, dateminute, datesecond, datemicrosecond)
    return interval
