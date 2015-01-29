"""
Script that wraps and steps through the dssg generation process.
"""

import sys

from .checks import source_dir_check
from .defaults import *


def execute_from_command_line():
    """
    Generate static site from command line with command `dssg <source-dir>`
    """
    source_dir_check()
