# Django settings for spadetree project.
import os, platform, socket

# Check environment
if os.environ.get('MYSITE_PRODUCTION', False):
    # Production
    DEBUG = TEMPLATE_DEBUG = False
    DEV   = False
    COMPRESS_ENABLED = True
else:
    # Development
    DEBUG = TEMPLATE_DEBUG = True
    DEV   = True
    COMPRESS_ENABLED = False

# Project name
project_name = 'spadetree'
project_root = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = MANAGERS = (
    ('Tommy Dang', 'quantumventuress@gmail.com')
)

AUTHENTICATION_BACKENDS = (
    'spadetree.backends.EmailAuthBackend',
    'spadetree.backends.FacebookAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)

COMPRESS_PRECOMPILERS = (
    ('text/coffeescript', 'coffee --compile --stdio'),
    ('text/x-scss', 'sass --scss {infile} {outfile}'),
)

if DEV:
    DATABASES_HOST = '' if platform.system() == 'Windows' else '192.168.1.70'
    DATABASES = {
        'default': {
            'ENGINE':   'django.db.backends.postgresql_psycopg2',
            'NAME':     'spadetree',
            'USER':     'postgres',
            'PASSWORD': 'postgres',
            'HOST':     DATABASES_HOST,
            'PORT':     '5432',
        }
    }
else:
    # Parse database configuration from $DATABASE_URL
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(default=os.environ['DATABASE_URL'])
    }

# Facebook
if DEV:
    FACEBOOK_APP_ID       = '144755539050891'
    FACEBOOK_APP_SECRET   = '9be888f73863e2962ff7a4109766acb9'
    FACEBOOK_REDIRECT_URI = 'http://localhost:8000/oauth/facebook/authenticate'
else:
    FACEBOOK_APP_ID       = '529124003816951'
    FACEBOOK_APP_SECRET   = 'fe72d3e9b55b01c0cb5ee1edc1684c7e'
    FACEBOOK_REDIRECT_URI = 'http://spadetree.com/oauth/facebook/authenticate'
FACEBOOK_SCOPE = ','.join([
    'email', 
    'user_about_me', 
    'user_interests', 
    'user_location'])

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Media
if DEV:
    MEDIA_ROOT = os.path.join(project_root, '..', 'media').replace(
        '\%s' % project_name, '/%s' % project_name)
else:
    MEDIA_ROOT = os.path.dirname(__file__).replace('\\', '/') + '/../media'

MEDIA_URL = '/media/'

USER_IMAGE_URL = '/img/users/'

if DEV:
    STATIC_ROOT = ''
    STATIC_URL  = '/static/'
else:
    STATIC_ROOT = os.path.dirname(__file__).replace('\\', '/') + '/..static'
    STATIC_URL  = 'http://s3.amazonaws.com/%s/' % project_name

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(project_root, '..', 'static').replace(
        '\\', '/').replace('\%s' % project_name, '/%s' % project_name),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '%ahnypdkx!!un2(ss$4co3*3o9(*t-w0$o$gitlvpn@4o#kfd9'

TEMPLATE_DIRS = (
    os.path.join(project_root, '..', 'templates').replace(
        '\\', '/').replace('\%s' % project_name, '/%s' % project_name),
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    # Pass MEDIA_URL through RequestContext
    'django.core.context_processors.media',
    # Pass request.user through RequestContext
    'django.core.context_processors.request',
    # Pass messages through RequestContext
    'django.contrib.messages.context_processors.messages',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# Message
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

ROOT_URLCONF = 'spadetree.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'spadetree.wsgi.application'

# Installed apps
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
)
# Utility apps
INSTALLED_APPS += (
    'compressor',
    'south',
)
# project apps
INSTALLED_APPS += (
    'cities',
    'interests',
    'oauth',
    'sessions',
    'skills',
    'states',
    'users',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
