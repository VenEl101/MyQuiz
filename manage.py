import os
import sys
import traceback
from config.env import get_env


def main():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        get_env("DJANGO_MODULE", default="config.settings.dev")
    )

    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Make sure it's installed and "
            "that your virtual environment is active."
        ) from exc


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Process interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print("\n💥 An unexpected error occurred:")
        traceback.print_exc()
        sys.exit(1)
