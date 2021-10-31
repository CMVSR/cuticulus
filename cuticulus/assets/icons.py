"""Emoji based icons module."""

import platform


class Icons(object):
    """Class for storing icons."""
    
    ismac = platform.system() == 'Darwin'
    islinux = platform.system() == 'Linux'
    iswindows = platform.system() == 'Windows'
    hassupport = islinux or ismac

    empty = ' '
    ant = '🐜' if hassupport else '(*Y*)'
    sound = '🔊' if hassupport else '<<'
