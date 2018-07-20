from config.settings import *
from django.utils.translation import ugettext_lazy as _
# Deactivate debug mode and debug toolbar in production
DEBUG = False
TEMPLATE_DEBUG = False
INTERNAL_IPS = []

ADMINS = (
    ('Lansana Sylla', 'lansanalsm@gmail.com'),
    ('Karifa Kouyate', 'vieuxkarifa@gmail.com'),
    ('Jules Thea', 'zakuijules@gmail.com'),
)

# Change our secret key in production
# SECRET_KEY = 'kjf2so%-1)kz(ejjm71l8^x(i22zr_bgh5ku+y)_g#o5y7*i*o'

LANGUAGE_CODE = 'fr-FR'
LANGUAGES = (
    ('fr', _('French')),
)

# Production Email Config GMAIL
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'smsi.budget@gmail.com'
# EMAIL_HOST_PASSWORD = 'Smsi2017'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = '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'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
