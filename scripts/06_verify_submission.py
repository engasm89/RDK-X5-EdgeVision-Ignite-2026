#!/usr/bin/env python3
"""Compatibility wrapper. Prefer 08_verify_submission.py."""
import runpy
from pathlib import Path
import sys

def main():
    namespace=runpy.run_path(str(Path(__file__).with_name('08_verify_submission.py')))
    return namespace['main']()

if __name__=='__main__':
    sys.exit(main())
