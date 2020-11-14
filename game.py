from collections import defaultdict
from json import dump, load
from os.path import isdir, isfile, join
from re import sub
from time import sleep, time

from __init__ import __version__
from func import clear, error, warn, acknow, input
from player import Player


class Game:
    def __init__(self, name, player=None):
        # load the assets
        self.story = {}
        self.load_story('intro')

        with open(join('assets', 'doc', 'game.txt')) as file:
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

        # initiate the game
        self.name = name

        if player is None:
            self.player = Player()
        else:
            self.player = player

        self.save()

    def save(self):
        with open(join('saves', f'{self.name}.json'), 'w') as file:
            dump(
                {
                    'player': self.player.dump()
                },
                file, indent=2, sort_keys=True)

    @classmethod
    def load(cls, name):
        path = join('saves', f'{name}.json')
        if isfile(path):
            with open(path) as file:
                game_data = load(file)

                if 'player' not in game_data:
                    error('Key "player" is not found in game data.')
                    return

                player = Player.load(game_data['player'])

                return cls(name, player)

        elif isdir(path):
            error('Game JSON should be a file.')

        else:
            error(f'File "{path}" is not found.')

    def load_story(self, name):
        with open(join('assets', 'story', f'{name}.txt')) as file:
            self.story[name] = file.read()

    @staticmethod
    def is_valid(data):
        if not isinstance(data, dict):
            return False

        if 'player' not in data:
            return False

        if not Player.is_valid(data['player']):
            return False

        return True

    def inform(self, name):
        if name not in self.story:
            error(f'Unknown story: "{name}"')
            return

        acknow(f'===== {name.capitalize()} =====')
        acknow('Use Ctrl+C to skip.')

        try:
            for ipara, para in enumerate(self.story[name].split('\n\n')):
                sleep(1)
                if ipara > 0:
                    for _ in range(2):
                        start = time()
                        acknow()
                        sleep(max(0, 0.25 - time() + start))
                for char in para:
                    start = time()
                    acknow(end=char, flush=True)
                    sleep(max(0, 0.05 - time() + start))

            sleep(1)

        except KeyboardInterrupt:
            acknow()

    def acknow(self, command=''):
        if command == '':
            acknow('Help on commands:')
            acknow(f'{self.doc}\n')
            acknow('Use "help <command>" for further documentation')
        else:
            if command in self.cmd_doc:
                acknow(f'Help on command "{command}":')
                acknow(f'{self.cmd_doc[command]}\n')
            else:
                error(f'Unknown command: "{command}"')

    def loop(self):
        acknow(f'Hackers {__version__}')
        acknow('Type "help" for more information.')

        while True:
            command = input('>> ')

            command = sub(r'\s+', command, r' ').strip()

            if command == 'exit':
                break

            elif command == 'clear':
                clear()

            elif command == 'help':
                self.acknow()

            elif command == 'read':
                error('Command "read" expected at least 1 argument, got 0')

            elif command == 'save':
                self.save()
                acknow('Saved!')

            elif command:
                parts = command.split()

                if parts[0] == 'help':
                    if len(parts) == 2:
                        self.acknow(parts[1])
                    else:
                        error(f'Command "help" expected at most 1 argument, '
                              f'got {len(parts) - 1}')

                elif parts[0] == 'read':
                    if len(parts) == 2:
                        self.inform(parts[1])
                    else:
                        error(f'Command "read" expected at most 1 argument, '
                              f'got {len(parts) - 1}')

                elif parts[0] in {'clear', 'exit', 'save'}:
                    error(f'Command "{parts[0]}" expected no argument, '
                          f'got {len(parts) - 1}')

                else:
                    error(f'Unknown command: "{parts[0]}"')

    def run(self):
        try:
            self.loop()
        except KeyboardInterrupt:
            print('\x1b[0m')
        finally:
            self.save()
            acknow('Saved!')
