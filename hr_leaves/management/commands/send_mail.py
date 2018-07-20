from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail, EmailMessage
from config import settings
from rh_leaves.models import SentMail
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
import datetime

class Command(BaseCommand):
    help = 'sending mail'

    def handle(self, *args, **options):
        """ Do your work here """
        WEEKEND = 6, 7
        count = 0
        self.stdout.write('executing....')
        #try:
        if datetime.datetime.now().isoweekday() not in WEEKEND:
            self.stdout.write('not weekend')
            get_submission_that_needs_reminder()
            get_submission_expired()
            get_agencys_expired()
            count += send_normals_emails()
            count += send_reminders_emails()
        else:
            print('Fuck out, this is a week end !')

        #except Exception as e: print('error message while sending email')
        self.stdout.write('There are {} email sent !'.format(count))

def get_submission_expired():
    flights = FlightSuggestion.objects.filter(user_validated=False)
    for alert in flights:
        interval = get_interval_from_date_to_now(alert.last_update_hours)
        now_hours = interval.seconds / 3600
        context = {
            'user': alert,
            'agency': alert.user.first_name
        }

        html_content = render_to_string('mails/submission_expired.html', context)

        if alert.valide < now_hours and not alert.expired and alert.mission.status == 3:
            mail = SentMail()
            mail.full_name = alert.user.get_full_name()
            mail.title = 'Soumission expirée'
            mail.email = alert.user.email
            mail.message = html_content
            mail.save()
            alert.expired = True
            alert.save()


def get_agencys_expired():
    agencys = User.objects.filter(is_agency=True, is_active=True, agence_expired=False)
    for agency in agencys:
        if agency.expired_date != None:
            interval = get_interval_from_date_to_now(agency.expired_date)
            now_hours = interval.seconds / 3600
            context = {
                'user': agency,
                'agency': agency.first_name
            }

            html_content = render_to_string(
                'mails/agency_expired.html', context)

            if now_hours > 0:
                mail = SentMail()
                mail.full_name = agency.get_full_name()
                mail.title = 'Quittance expirée'
                mail.email = agency.email
                mail.message = html_content
                mail.save()
                agency.agence_expired = True
                agency.save()


def send_normals_emails():
    # we get all normal emails and send them first
    normal_mails = SentMail.objects.filter(is_sent=False, is_repeated=False)
    count = 0

    for mail in normal_mails:
        send_email(mail)
        #mail.is_sent = True
        mail.save()
        count += 1
    return count

def send_reminders_emails():
    reminder_mails = SentMail.objects.filter(is_sent=False, is_repeated=True, is_MO_reminder_for_controler=False)
    count = 0
    for mail in reminder_mails:
        # for each email we try to get the interval since last sent
        interval = get_interval_from_date_to_now(mail.last_sent_at)
        interval_hours = (interval.seconds / 3600) + (interval.days * 24)
        #print('since last sent there is '+ str(interval_hours ) + ' hours')

        if interval_hours >= mail.sending_interval:
            # we send it
            send_email(mail)
            mail.number_sent += 1
            mail.last_sent_at = datetime.datetime.now()
            mail.save()
            count += 1

            if mail.number_sent >= 3 and mail.is_MO_reminder_for_user is True:
                controlers = User.objects.filter(is_controller=True)
                controlers_mails = SentMail.objects.filter(mission_id=mail.mission_id, is_MO_reminder_for_controler=True)

                if controlers and controlers_mails:
                    controlers_mail = controlers_mails[0]
                    for controler in controlers:
                        send_mail(
                            controlers_mail.title or 'ebiassy',
                            controlers_mail.message,
                            settings.EMAIL_HOST_USER,
                            (controler.email,),
                            fail_silently=False,
                            html_message=controlers_mail.message
                        )
                        controlers_mail.last_sent_at = datetime.datetime.now()
                        controlers_mail.save()
                        count += 1
    return count

# get 2 hours alertes
def get_submission_that_needs_reminder():

    missions = Mission.objects.filter(status=3)

    for mission in missions:
        flights_suggestions = FlightSuggestion.objects.filter(mission=mission, user_validated=False, is_active=True)
        if flights_suggestions.count() > 3:
            # then we get all the reminder emails for that mission
            # if the mission is opened for submissions
            mails = SentMail.objects.filter(mission_id=mission.id, is_sent=False, is_repeated=True)
            if not mails:
                # there is no repeated email for this mission
                # so let's create it
                context = {
                    'mission': mission
                    }
                html_content = render_to_string('mails/flight_submision_reminder.html', context)

                mail = SentMail()
                mail.full_name = mission.user.get_full_name()
                mail.title = _('Choosing a flight submission reminder')
                mail.email = mission.user.email
                mail.message = html_content
                mail.is_repeated = True
                mail.is_MS_reminder_for_user = True
                mail.mission_id = mission.id
                mail.last_sent_at = mission.created_at

                if mission.is_mission_urgent:
                    mail.sending_interval = 2
                else:
                    mail.sending_interval = 4
                mail.save()

# send and email object wich is comming from the db
def send_email(mail):
    if mail.flight_tichet:
        att_mail = EmailMessage(
            mail.title or 'ebiassy',
            mail.message,
            settings.EMAIL_HOST_USER,
            [mail.email],
        )
        att_mail.attach(mail.flight_tichet.name, mail.flight_tichet.read(), mail.flight_tichet_content_type)
        att_mail.content_subtype = 'html'
        att_mail.mixed_subtype = 'related'
        att_mail.send()
    else:
        # there is not attachement
        send_mail(
            mail.title or 'ebiassy',
            mail.message,
            settings.EMAIL_HOST_USER,
            (mail.email,),
            fail_silently=False,
            html_message=mail.message
        )

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
