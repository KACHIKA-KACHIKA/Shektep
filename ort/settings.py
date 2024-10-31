import os
from pathlib import Path
from dotenv import load_dotenv 
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

DEBUG = os.environ.get("DEBUG")

ALLOWED_HOSTS = [os.environ.get("ALLOWED_HOSTS")]

# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.sessions',
	
	'rest_framework',

	'videoplayer',
	'user',
	'exam',
	'serverpart',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'serverpart.middleware.CacheControlMiddleware',
]

ROOT_URLCONF = 'ort.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [
			BASE_DIR / 'serverpart/templates'
		],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
				'ort.context_processors.subscription_data',
			],
		},
	},
]

WSGI_APPLICATION = 'ort.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': os.environ.get("DB_ENGINE"),
		'NAME': os.environ.get("DB_NAME"),
		'USER': os.environ.get("DB_USER"),
		'PASSWORD': os.environ.get("DB_PASSWORD"),
		'HOST': os.environ.get("DB_HOST"),
		'PORT': os.environ.get("DB_PORT"),
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

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATICFILES_DIRS = [
	'static/',
]
STATIC_URL = 'static/'
# STATIC_ROOT= os.path.join(BASE_DIR, 'static/')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настройки для сессий
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Использовать базу данных для хранения сессий
SESSION_COOKIE_NAME = 'sessionid'  # Название куки-сессии
SESSION_COOKIE_AGE = 7200 #2 часа
SESSION_SAVE_EVERY_REQUEST = True  # Сохранять сессию на каждом запросе