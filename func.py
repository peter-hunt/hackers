from builtins import input as _input
from os import name, system
from re import match

__all__ = [
    'clear',
    'error',
    'request',
    'warn',
    'acknow',
    'input',
    'strict_input',
]


def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


def error(*args, sep=' ', end='\n', flush=False):
    content = sep.join(f'{arg}' for arg in args)
    print(end=f'\x1b[91m{content}{end}\x1b[0m', flush=flush)


def request(*args, sep=' ', end='\n', flush=False):
    content = sep.join(f'{arg}' for arg in args)
    print(end=f'\x1b[92m{content}{end}\x1b[0m', flush=flush)


def warn(*args, sep=' ', end='\n', flush=False):
    content = sep.join(f'{arg}' for arg in args)
    print(end=f'\x1b[93m{content}{end}\x1b[0m', flush=flush)


def acknow(*args, sep=' ', end='\n', flush=False):
    content = sep.join(f'{arg}' for arg in args)
    print(end=f'\x1b[96m{content}{end}\x1b[0m', flush=flush)


def strict_input(msg=None, pattern=r'[\s\S]*'):
    if msg is None:
        msg = ''

    while True:
        content = _input(f'\x1b[92m{msg}\x1b[1m')
        print(end='\x1b[0m')
        if match(pattern, content):
            return content
        else:
            warn(f'Input must match regex expression {pattern}')


def input(msg=None):
    if msg is None:
        content = _input('\x1b[0;1m')
    else:
        content = _input(f'\x1b[92m{msg}\x1b[0;1m')

    print(end='\x1b[0m')

    return content
