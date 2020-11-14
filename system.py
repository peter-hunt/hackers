from collections import defaultdict
from json import load
from json.decoder import JSONDecodeError
from os import walk
from os.path import isdir, isfile, join
from re import match, sub
from time import sleep, time

from __init__ import __version__
from func import clear, error, request, warn, acknow, input, strict_input
from game import Game


class System:
    def __init__(self):
        # load the assets
        with open(join('assets', 'doc', 'system.txt')) as file:
            doc = file.read()

        docs = sorted(doc.split('\n\n'),
                      key=lambda part: part.split('\n')[0])
        self.doc = '\n'.join(doc.split('\n')[0] for doc in docs)

        cmd_doc = defaultdict(list)

        for doc in docs:
            cmd = doc.split('\n')[0].split()[1]
            cmd_doc[cmd].append(doc)

        self.cmd_doc = {}
        for cmd in cmd_doc:
            self.cmd_doc[cmd] = '\n\n'.join(cmd_doc[cmd])

        with open(join('assets', 'warnings.txt')) as file:
            self.warnings = file.read().split('\n\n')

    def acknow(self, command=''):
        if command == '':
            acknow('Help on commands:')
            acknow(f'{self.doc}\n')
        else:
            if command in self.cmd_doc:
                acknow(f'Help on command "{command}":')
                acknow(f'{self.cmd_doc[command]}\n')
            else:
                error(f'Unknown command: "{command}"')

    def warn(self):
        try:
            for ipara, para in enumerate(self.warnings):
                if ipara == 0:
                    warn(end=para, flush=True)

                    for _ in range(2):
                        start = time()
                        warn()
                        sleep(max(0, 0.1 - time() + start))

                else:
                    sleep(0.5)

                    if ipara > 1:
                        for _ in range(2):
                            start = time()
                            warn()
                            sleep(max(0, 0.1 - time() + start))

                    for char in para:
                        start = time()
                        warn(end=char, flush=True)
                        sleep(max(0, 0.02 - time() + start))

            sleep(3)

        except KeyboardInterrupt:
            print(end='\x1b[0m')

    def create(self):
        try:
            request("Please enter the game's name.")
            name = strict_input(': ', r'^\S+$')

            Game(name)
        except KeyboardInterrupt:
            print('\x1b[0m')

    def list(self):
        for path in sorted(next(walk('saves'))[2]):
            if not match(r'^\S+\.json$', path):
                continue
            name = path[:-5]

            try:
                with open(join('saves', path)) as file:
                    data = load(file)
            except JSONDecodeError:
                error(f'  {name} (invalid JSON content)')
                continue

            if Game.is_valid(data):
                acknow(f'  {name}')
            else:
                error(f'  {name} (invalid game data)')

    def launch(self, name):
        game = Game.load(name)
        if game is not None:
            game.run()

    def loop(self):
        acknow(f'Hackers {__version__}')
        acknow('Type "help" for more information.')

        while True:
            command = input('> ')

            command = sub(r'\s+', command, r' ').strip()

            if command == 'exit':
                break

            elif command == 'clear':
                clear()

            elif command == 'create':
                self.create()

            elif command == 'help':
                self.acknow()

            elif command in {'list', 'ls'}:
                self.list()

            elif command in {'launch', 'run'}:
                error(f'Command "{command}" expected 1 argument, got 0')

            elif command:
                parts = command.split()

                if parts[0] == 'help':
                    if len(parts) == 2:
                        self.acknow(parts[1])
                    else:
                        error(f'Command "help" expected at most 1 argument, '
                              f'got {len(parts) - 1}')

                elif parts[0] in {'launch', 'run'}:
                    if len(parts) == 2:
                        self.launch(parts[1])
                    else:
                        error(f'Command "{parts[0]}" expected '
                              f'at most 1 argument, got {len(parts) - 1}')

                elif parts[0] in {'clear', 'create', 'exit', 'list', 'ls'}:
                    error(f'Command "{parts[0]}" expected no argument, '
                          f'got {len(parts) - 1}')

                else:
                    error(f'Unknown command: "{parts[0]}"')

    def run(self):
        clear()

        self.warn()

        clear()

        try:
            self.loop()
        except KeyboardInterrupt:
            print('\x1b[0m')
