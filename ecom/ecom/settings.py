"""
Django settings for ecom project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

import os
from django.contrib.messages import constants as messages

BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY = 'your_secret_key_here'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    # 'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'category',
    'accounts',
    'store',
    'admin_panel',
    'cart',
    'order',
    'userprofile',
    # 'login_app',
    
   
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecom.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'category.context_processors.menu_links',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecom.wsgi.application'

AUTH_USER_MODEL = "accounts.Account"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sparkle',
        'USER': 'postgres',
        'PASSWORD' : 'admin@123',
        'HOST' : 'localhost'
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
] 

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.joinpath('media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
    
}
SECRET_KEY ='$-c%$(7135)18qkt3aobof@7o=#pels1ty5@l!la4!*4*4d=vw'
DEBUG=True
EMAIL_HOST='smtp.gmail.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'aparnakj32@gmail.com'
EMAIL_HOST_PASSWORD = 'tuqhfpzzzulwzxjs'
EMAIL_USE_TLS = True

AUTHENTICATION_BACKENDS = [

    'accounts.backends.PhoneBackend',
    'django.contrib.auth.backends.ModelBackend',
] 

RAZORPAY_API_KEY = 'rzp_test_3Fn7H8WEqmzjzQ'
RAZORPAY_API_SECRET =  'KO1EefldMte8jsNMn7Lb7eLP'
SECURE_CROSS_ORIGIN_OPENER_POLICY='same-origin-allow-popups'

handler404 = 'ecom.views.handler404'

