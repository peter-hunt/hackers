from builtins import input as _input
from os import name, system as exe
from re import match

__all__ = [
    'clear',
    'error',
    'request',
    'warn',
    'system',
    'decide',
    'input',
    'strict_input',
]


def clear():
    if name == 'nt':
        exe('cls')
    else:
        exe('clear')


def error(*args, sep=' ', end='\n', flush=False):
    content = sep.join(f'{arg}' for arg in args)
    print(end=f'\x1b[0;91m{content}{end}\x1b[0m', flush=flush)


def request(*args, sep=' ', end='\n', flush=False):
    content = sep.join(f'{arg}' for arg in args)
    print(end=f'\x1b[0;92m{content}{end}\x1b[0m', flush=flush)


def warn(*args, sep=' ', end='\n', flush=False):
    content = sep.join(f'{arg}' for arg in args)
    print(end=f'\x1b[0;93m{content}{end}\x1b[0m', flush=flush)


def system(*args, sep=' ', end='\n', flush=False):
    content = sep.join(f'{arg}' for arg in args)
    print(end=f'\x1b[0;96m{content}{end}\x1b[0m', flush=flush)


def strict_input(msg=None, pattern=r'[\s\S]*'):
    if msg is None:
        msg = ''

    while True:
        content = _input(f'\x1b[92m{msg}\x1b[0;1;97m')
        print(end='\x1b[0m')
        if match(pattern, content):
            return content
        else:
            warn(f'Input must match regex expression {pattern}')


def decide(msg='', default=False):
    choices = '[Y/n]' if default else '[y/N]'

    if msg.strip() == '':
        prompt = f'\x1b[92m{choices}> \x1b[0;1;97m'
    else:
        prompt = f'\x1b[92m{msg} {choices}> \x1b[0;1;97m'

    while True:
        content = _input(prompt)
        print(end='\x1b[0m')

        result = {'': default, 'y': True, 'n': False}.get(content.lower())

        if result is not None:
            return result

        error('Invalid choice. Please try again.')


def input(msg=None):
    if msg is None:
        content = _input('\x1b[0;1;97m')
    else:
        content = _input(f'\x1b[92m{msg}\x1b[0;1;97m')

    print(end='\x1b[0m')

    return content
