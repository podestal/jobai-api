from .base import *
import os

DEBUG = True

# Get ALLOWED_HOSTS from environment variable
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '*').split(',')
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS if host.strip()]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASS'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# CORS Configuration - Get from environment variable
cors_origins = os.getenv('DJANGO_CORS_ALLOWED_ORIGINS', 'http://localhost:5173')
CORS_ALLOWED_ORIGINS = [
    origin.strip() 
    for origin in cors_origins.split(',') 
    if origin.strip()
]

CORS_ALLOW_CREDENTIALS = True

# Allow all origins in development (optional - remove if you want strict control)
# CORS_ALLOW_ALL_ORIGINS = DEBUG