#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

""" 
This app has been done by software engineering international students as final project of web development course
The app developed by:
- SAID SAIF MOHAMMED ALSAIDI
- MOHAMMED SAAD
- AMMAR KHALID
- HIDER 

"""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sindibad_tour_guide.settings')
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
