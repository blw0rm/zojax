import sys, os
from django.conf import global_settings

PROJECT_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../../')
ugettext = lambda s: s

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Admin', 'admin@example.com'),
)

MANAGERS = ADMINS


DATABASES = {
    'default': {
        'NAME': 'db',                           # Or path to database file if using sqlite3.
        'ENGINE': 'django.db.backends.sqlite3', # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'USER': '',                             # Not used with sqlite3.
        'PASSWORD': '',                         # Not used with sqlite3.
    },
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-en'

LANGUAGES = (
    ('en', ugettext('English')),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
#USE_L10N = True

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

SERVE_STATIC = True

STATICFILES_FINDERS = (
  "django.contrib.staticfiles.finders.FileSystemFinder",
  "django.contrib.staticfiles.finders.AppDirectoriesFinder",
  "zojax.finders.AppMediaDirectoriesFinder"
)


#ADMIN_MEDIA_PREFIX = '/amedia/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'w-fd5ujpeneh@)44sn-lasyrlshdjf4k*)(#kru*ls6jo5^!ol^kwuq4z+j(w'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    (#'django.template.loaders.cached.Loader',
    (
        'django.template.loaders.app_directories.Loader',
        'django.template.loaders.eggs.Loader',
    )),
)

MIDDLEWARE_CLASSES = (
    #'django.middleware.cache.UpdateCacheMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'annoying.middlewares.RedirectMiddleware',

#     'debug_toolbar.middleware.DebugToolbarMiddleware',
#    'django.middleware.cache.FetchFromCacheMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'publicauth.PublicBackend',
)


ROOT_URLCONF = 'zojax.urls'


INSTALLED_APPS = (
    #Own
    'zojax',
    
    #Built-in
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #External
    'publicauth',
    'debug_toolbar',
    

)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'django.core.context_processors.csrf',
#    'django.core.context_processors.static',
    'django.core.context_processors.debug',
)

TEST_RUNNER = "zojax.tests.coverage_runner.run_tests"
COVERAGE_REPORT_PATH = os.path.join(PROJECT_ROOT, 'coverage_report')

#CACHE_MIDDLEWARE_SECONDS = 5
#CACHE_MIDDLEWARE_KEY_PREFIX = ''
#CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/account/login/'
LOGOUT_URL = '/account/logout/'

# debug toolbar
INTERNAL_IPS = ('127.0.0.1', )
DEBUG_TOOLBAR_PANELS = (
        #'debug_toolbar.panels.version.VersionDebugPanel',
        'debug_toolbar.panels.timer.TimerDebugPanel',
        #'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
        'debug_toolbar.panels.headers.HeaderDebugPanel',
        'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
        'debug_toolbar.panels.template.TemplateDebugPanel',
        'debug_toolbar.panels.sql.SQLDebugPanel',
        #'debug_toolbar.panels.cache.CacheDebugPanel',
        #'debug_toolbar.panels.signals.SignalDebugPanel',
        'debug_toolbar.panels.logger.LoggingPanel',
)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request':{
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


# Amazon S3 settins
DEFAULT_FILE_STORAGE = 'storages.backends.s3.S3Storage'
AWS_ACCESS_KEY_ID = "PLACE YOUR KEY ID HERE"
AWS_SECRET_ACCESS_KEY = "PLACE YOUR SECRET ACCESS EY"
AWS_STORAGE_BUCKET_NAME = "zojax"

from S3 import CallingFormat

AWS_CALLING_FORMAT = CallingFormat.SUBDOMAIN


# OpenID & OAuth settings
PUBLICAUTH_EXTRA_FORM = 'zojax.forms.ExtraForm'
PUBLICAUTH_ACTIVATION_REQUIRED = False

#API_KEY = "DAtsOy4KRonlpuPTfb6Miw"
# https://dev.twitter.com/apps/1045770
#
TWITTER_PROFILE_MAPPING = { 'screen_name': 'username', }

GOOGLE_PROFILE_MAPPING = {
    'email': 'email',
    'fullname': 'last_name',
    }

FILE_PREVIEW_URL = "https://docs.google.com/viewer?embedded=true&url="

try:
    from .local import *
except ImportError:
    pass

ADMIN_MEDIA_PREFIX = STATIC_URL+'admin/'