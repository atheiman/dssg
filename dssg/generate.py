"""
Script that wraps and steps through the dssg generation process.
"""

from .checks import check_all
from .defaults import *


def generate(source_dir):
    """
    Generate static site from command line with command `dssg <source-dir>`
    """
    check_all(source_dir)
