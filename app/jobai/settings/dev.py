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

# CLOUDFLARE SETUP

CLOUDFLARE_R2_BUCKET = os.environ.get('CLOUDFLARE_R2_BUCKET')
CLOUDFLARE_R2_ACCESS_KEY= os.environ.get('CLOUDFLARE_R2_ACCESS_KEY')
CLOUDFLARE_R2_SECRET_KEY = os.environ.get('CLOUDFLARE_R2_SECRET_KEY')
CLOUDFLARE_R2_ENDPOINT = os.environ.get('CLOUDFLARE_R2_ENDPOINT')

STORAGES = {
    # Media files (user uploads) -> Cloudflare R2
    'default': {
        'BACKEND': 'storages.backends.s3.S3Storage',
        'OPTIONS': {
            'access_key': CLOUDFLARE_R2_ACCESS_KEY,
            'secret_key': CLOUDFLARE_R2_SECRET_KEY,
            'endpoint_url': CLOUDFLARE_R2_ENDPOINT,
            'bucket_name': CLOUDFLARE_R2_BUCKET,
            'default_acl': 'public-read',  # or 'private'
            'region_name': 'auto',         # R2 ignores this but boto3 needs it
            'signature_version': 's3v4',
        },
    },
    # Static files (CSS, JS, etc.) -> Local storage (as before)
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
}


