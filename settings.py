# $Id$
DEBUG = True
TEMPLATE_DEBUG = DEBUG

if not DEBUG:
	LOGIN_URL = '/hivapp/accounts/login'
	LOGOUT_URL = '/hivapp/accounts/logout'
	LOGIN_REDIRECT_URL = '/hivapp/'
	SESSION_COOKIE_SECURE = True

ADMINS = (
    ('Sean M. Collins', 'sean@coreitpro.com'),
)

if DEBUG:
	MANAGERS = ADMINS
	DATABASE_ENGINE = 'mysql'
	DATABASE_NAME = 'hivapp'
	DATABASE_USER = 'root'
	DATABASE_PASSWORD = 'root'
	DATABASE_HOST = ''
	DATABASE_PORT = '8889'
else:
	DATABASE_ENGINE= "mysql"
	DATABASE_NAME = 'hivapp'
	DATABASE_USER = 'hivapp'
	DATABASE_HOST = 'localhost'
	DATABASE_PASSWORD = 'ZTrMs1iCb'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
if DEBUG:
	MEDIA_ROOT = "/Users/scollins/Programming/CoreITPro/BTech/hivapp/helix/media"
else:
	MEDIA_ROOT = "/var/www/html/media"



# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site_media/'


# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
if DEBUG:
	ADMIN_MEDIA_PREFIX = '/media/'
else:
	ADMIN_MEDIA_PREFIX = '/media/admin/'


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'h6zsd-$u&pe=kop$1q6u^ykg#-=b)&gaxjy-wh0cn@^o^^w7$)'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.eggs.load_template_source',
)

'''

http://djangobook.com/en/2.0/chapter17/

The order is significant. On the request and view phases,
Django applies middleware in the order given in MIDDLEWARE_CLASSES,
and on the response and exception phases, Django applies middleware
in reverse order. That is, Django treats MIDDLEWARE_CLASSES
as a sort of wrapper around the view function: on the request
it walks down the list to the view, and on the response it walks back up.


'''
MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
        'django.middleware.transaction.TransactionMiddleware',
    'reversion.middleware.RevisionMiddleware',
    
)

ROOT_URLCONF = 'helix.urls'

if DEBUG:
	TEMPLATE_DIRS = (
    		# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    		# Always use forward slashes, even on Windows.
    		# Don't forget to use absolute paths, not relative paths.
    		'/Users/scollins/Programming/CoreITPro/BTech/hivapp/helix/templates/',
	)
else:
	TEMPLATE_DIRS = ('/var/www/html/hivapp/helix/templates/')



INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'hiv',
    'reversion',
)
