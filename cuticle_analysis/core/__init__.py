
import logging
import os
import sys

import colorama
from colorama import Fore

from .arguments import get_args
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

    args = get_args()

    if args.download_dataset:
        from .dataset import download_dataset, unzip_dataset
        download_dataset()
        unzip_dataset()

    else:
        dataset_setup()
