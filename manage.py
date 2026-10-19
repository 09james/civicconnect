#!/usr/bin/env python
"""Run administrative tasks for the public service portal."""

import os
import sys


def main():
    """Execute Django's command-line utility."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "service_portal.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django is not installed. Install the project requirements first."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
