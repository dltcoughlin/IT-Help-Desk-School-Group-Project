#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import dotenv

def main():
    """Read environment variables"""
    django_env = None
    if ('DJANGO_ENV' in os.environ):
        django_env = os.getenv('DJANGO_ENV')
    dotenv.read_dotenv()
    if (django_env != None):
        os.environ['DJANGO_ENV'] = django_env

    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
