from .base import *

# =====================
# STATIC & MEDIA
# =====================
STATIC_URL = "/static/"
MEDIA_URL = "/media/"

STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_ROOT = BASE_DIR / "mediafiles"


# Developer specific settings
# CORS_ALLOW_ALL_ORIGINS = True
