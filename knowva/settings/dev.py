from .base import *

SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBBUG') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')

DATABASES = {
    'default': {
        'ENGINE': os.getenv('ENGINE'),
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}