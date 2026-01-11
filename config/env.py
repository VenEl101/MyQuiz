from decouple import config, UndefinedValueError
from django.core.exceptions import ImproperlyConfigured


REQUIRED_ENVS = [
    # Basic
    "DJANGO_SECRET",
    "DJANGO_DEBUG",
    "DB_NAME",
    "PG_USER",
    "PG_PASSWORD",
    "DJANGO_MODULE",
]


def get_env(name, cast=str, required=False, default=None):
    try:
        value = config(name, cast=cast)
    except UndefinedValueError:
        if required:
            raise ImproperlyConfigured(f"❌ Required ENV `{name}` is missing in .env")
        return default
    except Exception as e:
        raise ImproperlyConfigured(f"❌ ENV error for {name}: {str(e)}")

    if required and (value is None or value == "" or value == " "):
        raise ImproperlyConfigured(f"❌ Required ENV `{name}` is empty or invalid")

    return value
