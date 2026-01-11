from .base import *

DEBUG = True

# DEBUG = False
# ALLOWED_HOSTS = ["yourdomain.com", "www.yourdomain.com"]

# STATIC & MEDIA - production server uchun
STATIC_URL = "/static/"
MEDIA_URL = "/media/"

STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_ROOT = BASE_DIR / "mediafiles"


