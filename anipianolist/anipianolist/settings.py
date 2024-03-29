"""
Django settings for anipianolist project.

Generated by 'django-admin startproject' using Django 4.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os 
import environ

env = environ.Env(
    DEBUG=(bool, False)
)

environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

# Application definition

INSTALLED_APPS = [
    # our own apps (accounts, base) MUSTTTTT be above allauth.* to take precedence
    # please keep keqing happy by ensuring this!
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'accounts',
    'base', 
    'database',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.discord',
    'allauth.socialaccount.providers.google',
    'auditlog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'auditlog.middleware.AuditlogMiddleware',
]

ROOT_URLCONF = 'anipianolist.urls'

LOGIN_REDIRECT_URL = '/login/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates' ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
]

WSGI_APPLICATION = 'anipianolist.wsgi.application'

SITE_ID = 1

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USERNAME'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '',
    }
}

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS_ARRAY')

SOCIALACCOUNT_PROVIDERS = {
    # For each OAuth based provider, either add a ``SocialApp``
    # (``socialaccount`` app) containing the required client
    # credentials, or list them here:
    'discord': {
        'APP': {
            'client_id': env('DISCORD_OAUTH2_CLIENT_ID'),
            'secret': env('DISCORD_OAUTH2_CLIENT_SECRET'),
            'key': ''
        }
    },
    'google': {
        'APP': {
            'client_id': env('GOOGLE_OAUTH2_CLIENT_ID'),
            'secret': env('GOOGLE_OAUTH2_CLIENT_SECRET'),
            'key': ''
        }
    }
}

SOCIALACCOUNT_AUTO_SIGNUP = True
ACCOUNT_AUTHENTICATION_METHOD = "username"
ACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_EMAIL_REQUIRED = False
SOCIALACCOUNT_EMAIL_REQUIRED = False

GOOGLE_API_KEY = env('GOOGLE_API_KEY')

YOUTUBE_API_INSTANCE = env('YOUTUBE_API_INSTANCE')

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_ROOT = BASE_DIR / "../static"
STATIC_URL = 'static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, '../static/css/'),
    os.path.join(BASE_DIR, '../static/css/pico/'),
    os.path.join(BASE_DIR, '../static/css/pico/themes/'),
    os.path.join(BASE_DIR, '../static/svg/'),
    os.path.join(BASE_DIR, '../static/js/'),
    os.path.join(BASE_DIR, '../static/img/'),
    os.path.join(BASE_DIR, '../static/img/httpresponse/'),
    os.path.join(BASE_DIR, '../static/highlightjs/'),
    os.path.join(BASE_DIR, '../static/highlightjs/styles/'),
    os.path.join(BASE_DIR, '../static/highlightjs/languages/')
)

# i literally have no idea what is going on here but i will fix this later :KEKW:

## Media uploads

MEDIA_ROOT = BASE_DIR / "../media"
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

## Group names

MAINTAINER_GROUP = env('MAINTAINER_GROUP')
MODERATOR_GROUP = env('MODERATOR_GROUP')
ADMIN_GROUP = env('ADMIN_GROUP')

DJANGO_HASHIDS_SALT = env('HASHID_SALT')

AUDITLOG_INCLUDE_ALL_MODELS=False