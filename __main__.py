"""
Hackers
  Command-line adventure game written in Python 3

Usage:
  hackers [options]

Options:
  -h, --help     Show this help message and exit
  -v, --version  Show the version and exit
"""


from docopt import docopt

from __init__ import __version__
from game import Game


def main():
    docopt(__doc__, version=f'Hackers {__version__}')
    Game().loop()


if __name__ == '__main__':
    main()
