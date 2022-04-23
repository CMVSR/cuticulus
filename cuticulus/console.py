"""Global console module."""

import logging
import os

from dotenv import load_dotenv
from rich.console import Console
from rich.logging import RichHandler


load_dotenv('.env')


def log_level(console: Console, level: str):
    """Print logging level.

    Args:
        console (Console): Console object.
        level (str): Log level.
    """
    text = 'LOG LEVEL: "{0}"'.format(level)
    console.log(text)


def init_console() -> Console:
    """Initialize console.

    Returns:
        Console: Console object.
    """
    return Console()


def init_logger(console: Console):
    """Initialize logger.

    Args:
        console (Console): Console object.
    """
    level = os.getenv('LOG_LEVEL', 'INFO')

    logging.basicConfig(
        level=logging.getLevelName(level),
        format='%(message)s',
        datefmt='[%X]',
        handlers=[RichHandler()],
    )

    log_level(console, level)


console = init_console()
init_logger(console)
