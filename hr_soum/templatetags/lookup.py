from django  import template
from django.contrib.humanize.templatetags.humanize import intcomma
from .. import models
from django.utils.translation import ugettext_lazy as _

register = template.Library()
@register.filter
def lookup(d, key):
    try:
        if len(d) >= key:
            return d[key]
        else:
            return None
    except:
        return None

# get if there is at least one suggestion that is validated
# by the admin
@register.filter
def at_least_one_admin_validated(data):
    for elem in data:
        if elem.admin_validated:
            return True
    return False

@register.filter
def personnes(value, user):
    """Removes all values of arg from the given string"""
    return models.Personne.objects.all() if user.is_admin or user.is_controller else models.Personne.objects.filter(ministry_id=user.ministry)

@register.filter
def filter_users(value):
    """Removes all values of arg from the given string"""
    return models.User.objects.filter(is_controller=False, is_admin=False)


@register.filter
def prepend_dollars(dollars):
    if dollars:
        dollars = round(float(dollars), 2)
        return "$%s%s" % (intcomma(int(dollars)), ("%0.2f" % dollars)[-3:])
    else:
        return ''


@register.filter
def prepend_gnf(gnf):
    if gnf:
        gnf = round(float(gnf), 2)
        return "%s%s GNF" % (intcomma(int(gnf)), ("%0.2f" % gnf)[-3:])
    else:
        return ''

@register.filter
def format_status(status):
    if status == 0:
        return _("Pending")
    elif status == 1:
        return _("Approuved")
    elif status == 2:
        return _("Rejected")
    else:
        return 'Unknow'
