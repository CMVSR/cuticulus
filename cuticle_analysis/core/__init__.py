
import logging
import os
import sys

import colorama
from colorama import Fore

from .dataset import dataset_setup
from .display import description, debug_mode


def init():
    colorama.init(wrap=True)
    description()

    levels = ['NOTSET', 'WARN', 'INFO', 'DEBUG']
    level = os.getenv('LOG_LEVEL')

    if not level:
        level = 'NOTSET'
    if level != 'NOTSET':
        os.environ['debug_mode'] = 'yes'
        logging.basicConfig(
            level=logging.getLevelName(level),
            format=Fore.CYAN + '%(asctime)s '
            + Fore.RED + '[%(levelname)s] '
            + Fore.YELLOW + '(%(name)s)\n'
            + Fore.WHITE + '%(message)s' + Fore.RESET,
        )
        debug_mode(level)


def start_app():
    init()
    dataset_setup()
