from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
from backend.settings import get_secret

SECRET_KEY = get_secret("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]
# ALLOWED_HOSTS = [get_secret("ALLOWED_HOST")]

FIREBASE_CONFIG = {
    "apiKey": get_secret("FIREBASE_API_KEY"),
    "authDomain": get_secret("FIREBASE_AUTH_DOMAIN"),
    "projectId": get_secret("FIREBASE_PROJECT_ID"),
    "storageBucket": get_secret("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": get_secret("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": get_secret("FIREBASE_APP_ID"),
    "databaseURL": get_secret("FIREBASE_DATABASE_URL"),
}

API_KEY = get_secret("API_KEY")
API_SECRET_KEY = get_secret("API_SECRET_KEY")
