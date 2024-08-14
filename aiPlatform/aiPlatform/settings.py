"""
Django settings for aiPlatform project.

Generated by 'django-admin startproject' using Django 4.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = '/static/' # 别名 
STATICFILES_DIRS = [ 
    os.path.join(BASE_DIR, "aiPlatform/static"), 
]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-o-n_dp+$puadvk14z^t)*k#9f!z2bjo=_eblof8o8!03413p)o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']





# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap5',
    'aiPlatformImplement',
    'django.urls',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'aiPlatform.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'aiPlatform.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'AISYSPLUS',
    'USER':'root',
    'PASSWORD':'PASSWORD',
    'HOST':'101.37.208.190',
    'PORT':'3306',
    'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/aiPlatform/static/'
STATICFILES_DIRS = [
       os.path.join(BASE_DIR, "aiPlatform/static"),
   ]
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
TIME_ZONE = 'Asia/Shanghai'

WEBSITE_ADDRESS = 'http://223.8.79.23:8000'

ALIPAY_PUBLIC_KEY = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA8LNH7i4jvRBIT7sQVSgc5zZVHfI3CAaseu8QfsRjsdTgHVzAz19ZlWmFiobv7HcvS0SFDxdgMQ+IgiRXLfEUXQyBHXk8kVjXchUoQs57POn2phGvn4iFECQ1FGJQtVCi7RVQU+yMRLr6gsdY1BF1WapwpS5bhXCZXvoXOoN38HuRzHjfMo714wuXjzYN6w8MI4GSBACv/zuq94phd21xy4O7QIblqtZXCTnWiYwUqcTmX0vqR0I0sHEoQHhPb5Pz02yfibn67DKQFpiZ0U0Ygf9ta8SAI+O4yMPjWWiYUDrNlQeDik+oP8qdjlInqFQ3PBcfhrKmYi0QFO1QgNvFkwIDAQAB'