from config.settings import *
import dj_database_url

# Deactivate debug mode and debug toolbar in production
DEBUG = False
TEMPLATE_DEBUG = False
INTERNAL_IPS = []


# Allow heroku host to execture our app
ALLOWED_HOSTS = [
    'rh_leaves.herokuapp.com',
]

# Change our secret key in production
#SECRET_KEY = 'kjf2so%-1)kz(ejjm71l8^x(i22zr_bgh5ku+y)_g#o5y7*i*o'
DATABASES['default'] = dj_database_url.config()
