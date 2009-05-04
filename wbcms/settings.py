# Django settings for wbcms project.

import os

try:
    from local_settings import PROJECT_NAME, PROJECT_PATH, PROJECT_URL, DEBUG
except ImportError, e:
    DEBUG = False
    PROJECT_NAME = os.path.split(os.path.dirname(os.path.abspath(__file__)))[-1]
    PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
    PROJECT_URL = 'http://localhost:8002'

def _PATH(*args):
    return os.path.join(PROJECT_PATH, *args)

def _URL(*args):
    return os.path.join(*args)

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = _PATH('var','testdb.sqlite')             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = _PATH('media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = "http://media.ts.wrd.nu/media/"

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = 'http://media.ts.wrd.nu/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '7%lj)m#%(d8=2g&vcw4k1w@a4pgp%w!$eep4$bsa20+5h02d-s'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.contrib.csrf.middleware.CsrfMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'cms.middleware.util.XHTMLToHTMLMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    #'pagination.middleware.PaginationMiddleware'
)

ROOT_URLCONF = '.'.join([PROJECT_NAME, 'urls'])

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    _PATH(PROJECT_NAME,'templates'),
    _PATH(PROJECT_NAME,'templates','yui')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admindocs',
    'django.contrib.flatpages',
    'tiger',
    'cms',
    'django_extensions',
    'registration',
    'profiles',
    'utils',
    'django.contrib.admin',
)

CMS_DEFAULT_TEMPLATE = 'base_cms.html'
CMS_LANGUAGE_REDIRECT = False
CMS_USE_TINYMCE = False


AUTH_PROFILE_MODULE = 'tiger.Person'
LOGIN_URL = '/login'
LOGOUT_URL = '/logout'

ACCOUNT_ACTIVATION_DAYS = 3

MEDIA_URL="http://media.ts.wrd.nu/media/"


INTERNAL_IPS = ('127.0.0.1',)
LANGUAGES = (
    ('en', 'English'),
)



try:
    from local_settings import *
except:
    pass
