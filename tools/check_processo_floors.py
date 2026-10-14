#!/usr/bin/env python3
"""Compatibility entry point for the Processo Civil I course floors."""
import sys
from check_course_floors import main

if __name__ == "__main__":
    sys.argv.insert(1, "processo-civil-i")
    raise SystemExit(main())
