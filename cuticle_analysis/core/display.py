
from colorama import Fore

from ..assets.icons import Icons

LINE_SIZE = 80


def description():
    print('=' * LINE_SIZE)
    title = Icons.ANT + ' Cuticle Analysis ' + Icons.ANT
    padding = ' ' * ((LINE_SIZE - len(title)) // 2)
    print(Fore.YELLOW, padding + title, Fore.RESET)

    print('=' * LINE_SIZE)
    desc = 'https://github.com/ngngardner/cuticle_analysis'
    padding = ' ' * ((LINE_SIZE - len(desc)) // 2)
    print(Fore.CYAN, padding + desc, Fore.RESET)
    print('-' * LINE_SIZE)


def debug_mode(level):
    text = Fore.RED + ' ' + Icons.SOUND + ' '
    text += 'LOG LEVEL: %s' % level
    text += Fore.RESET

    padding = ' ' * ((LINE_SIZE - len(text)) // 2)
    print(padding + text)

    print('-' * LINE_SIZE)
