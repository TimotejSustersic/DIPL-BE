from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
from backend.settings import get_secret

SECRET_KEY = get_secret("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]
# ALLOWED_HOSTS = [get_secret("ALLOWED_HOST")]

DB_CONFIG = {
    'ENGINE': 'django.db.backends.postgresql',
    "HOST": get_secret("CLOUD_SQL_CONNECTION_NAME"),
    "NAME": get_secret("DB_NAME"),
    "USER": get_secret("DB_USER"),
    "PASSWORD": get_secret("DB_PASSWORD"),
    'PORT': '5432',  # Default port for PostgreSQL
}

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': DB_CONFIG
}