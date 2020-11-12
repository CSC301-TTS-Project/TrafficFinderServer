#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import coverage
import django


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'traffic_finder_server.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    django.setup()

    is_testing = 'test' in sys.argv
    if is_testing:
        cov = coverage.coverage(source=['api'], omit=['*/tests/*'])
        cov.set_option('report:show_missing', True)
        cov.erase()
        cov.start()
    # Add this 5 line above
    execute_from_command_line(sys.argv)
    # and add this 4 line below
    if is_testing:
        cov.stop()
        cov.save()
        cov.report()


if __name__ == '__main__':
    main()
