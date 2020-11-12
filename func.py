from os import name, system
from re import escape, match

__all__ = [
    'clear',
    'error',
    'warn',
    'acknow',
]


def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


def error(*args, sep=' ', end='\n', flush=False):
    content = sep.join(f'{arg}' for arg in args)
    print(end=f'\x1b[91m{content}{end}\x1b[0m', flush=flush)


def warn(*args, sep=' ', end='\n', flush=False):
    content = sep.join(f'{arg}' for arg in args)
    print(end=f'\x1b[93m{content}{end}\x1b[0m', flush=flush)


def acknow(*args, sep=' ', end='\n', flush=False):
    content = sep.join(f'{arg}' for arg in args)
    print(end=f'\x1b[96m{content}{end}\x1b[0m', flush=flush)


def strict_input(msg=None, pattern=r'[\s\S]*'):
    if msg is None:
        msg = ': '
    elif not msg.endswith(': '):
        msg = f'{msg.rstrip()}: '

    while True:
        content = input(msg)
        print(end='\x1b[0m')
        if match(content, match):
            return content
        else:
            warn(f'Input must match regex expression {escape(pattern)}')
