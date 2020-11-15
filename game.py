from collections import defaultdict
from json import dump, load
from os.path import isdir, isfile, join
from re import match, sub
from time import sleep, time

from __init__ import __version__
from func import clear, error, request, warn, system, input
from npc import Npc
from player import Player


class Game:
    def __init__(self, name, player=None, npc=None):
        self.story = {}
        self.load_story('intro')

        with open(join('assets', 'doc', 'game.txt')) as file:
            doc = file.read()

        docs = sorted(doc.split('\n\n'),
                      key=lambda part: part.split('\n')[0])
        self.doc = '\n'.join(doc.split('\n')[0] for doc in docs)

        cmd_doc = defaultdict(list)

        for doc in docs:
            parts = doc.split('\n')[0].split()
            cmd = parts[1]

            for part in parts[2:]:
                if part.startswith('<'):
                    break
                cmd = f'{cmd} {part}'

            cmd_doc[cmd].append(doc)

        self.cmd_doc = {}
        for cmd in cmd_doc:
            self.cmd_doc[cmd] = '\n\n'.join(cmd_doc[cmd])

        self.name = name

        if player is None:
            self.player = Player()
        else:
            self.player = player

        if npc is None:
            self.npc = Npc()
        else:
            self.npc = npc

        self.save()

    def save(self):
        with open(join('saves', f'{self.name}.json'), 'w') as file:
            dump({
                'npc': self.npc.dump(),
                'player': self.player.dump()
            }, file, indent=2, sort_keys=True)

    @classmethod
    def load(cls, name):
        path = join('saves', f'{name}.json')

        if isfile(path):
            with open(path) as file:
                data = load(file)

                if not cls.is_valid(data):
                    return

                player = Player.load(data['player'])
                npc = Npc.load(data['npc'])

                return cls(name=name, player=player, npc=npc)

        elif isdir(path):
            error('Game data should be a file.')

        else:
            error(f'File "{path}" is not found.')

    def load_story(self, name):
        with open(join('assets', 'story', f'{name}.txt')) as file:
            self.story[name] = file.read()

    @staticmethod
    def is_valid(data, *, alert=True):
        if not isinstance(data, dict):
            if alert:
                error(f'Game data should be a dictionary, '
                      f'not "{type(data).__name__}".')
            return False

        if 'player' not in data:
            if alert:
                error('Key "player" is not found in game data.')
            return False

        if not Player.is_valid(data['player'], alert=alert):
            return False

        if 'npc' not in data:
            if alert:
                error('Key "npc" is not found in game data.')
            return False

        if not Npc.is_valid(data['npc'], alert=alert):
            return False

        return True

    def inform(self, name):
        if name not in self.story:
            error(f'Unknown story: "{name}"')
            return

        system(f'===== {name.capitalize()} =====')
        system('Use Ctrl+C to skip.')

        try:
            for ipara, para in enumerate(self.story[name].split('\n\n')):
                sleep(1)
                if ipara > 0:
                    for _ in range(2):
                        start = time()
                        system()
                        sleep(max(0, 0.25 - time() + start))
                for char in para:
                    start = time()
                    system(end=char, flush=True)
                    sleep(max(0, 0.05 - time() + start))

            sleep(1)

        except KeyboardInterrupt:
            system()

    def acknow(self, cmd=''):
        if cmd == '':
            system('Help on commands:')
            system(self.doc)
            system('Use "help <command>" for further documentation')
        else:
            if cmd in self.cmd_doc:
                system(f'Help on command "{cmd}":')
                for key in self.cmd_doc:
                    if key.split()[0] == cmd:
                        system(self.cmd_doc[key])
            else:
                error(f'Unknown command: "{cmd}"')

    def loop(self):
        system(f'Game "{self.name}"')
        system('Type "help" for more information.')

        while True:
            command = input('>> ')

            command = sub(r'\s+', command, r' ').strip()

            if command in {'attr', 'attribute'}:
                self.player.attribute()

            elif command == 'clear':
                clear()

            elif command == 'exit':
                break

            elif command == 'help':
                self.acknow()

            elif command in {'deposit', 'read', 'withdraw'}:
                error(f'Command "{command}" expected '
                      f'at least 1 argument, got 0')

            elif command == 'resource':
                self.player.resource()

            elif command == 'save':
                self.save()
                system('Successfully saved the game!')

            elif command == 'status':
                self.player.status()

            elif command:
                parts = command.split()

                if parts[0] == 'help':
                    self.acknow(' '.join(parts[1:]))

                elif parts[0] == 'deposit':
                    if len(parts) != 2:
                        error(f'Command "deposit" expected '
                              f'1 argument, got {len(parts) - 2}')
                        continue

                    if parts[1] == 'all':
                        amount = self.player.purse
                    elif parts[1] == 'half':
                        amount = round(self.player.purse / 2, 2)
                    elif match(r'^\d+('
                               r'(\.\d{0,2})|((\.\d{0,5})?k)'
                               r'|((\.\d{0,8})?m)|((\.\d{0,11})?b)'
                               r'|((\.\d{0,14})?t)'
                               r')?$', parts[1]):
                        if parts[1][-1] in {'k', 'm', 'b', 't'}:
                            amount = float(parts[1][:-1]) * {
                                'k': 1_000,
                                'm': 1_000_000,
                                'b': 1_000_000_000,
                                't': 1_000_000_000_000,
                            }[parts[1][-1]]
                        else:
                            amount = float(parts[1])
                    else:
                        error(f'Invalid amount: {parts[1]}')
                        continue

                    if amount > self.player.purse:
                        warn('Not enough money in your purse.')
                        continue

                    self.player.purse -= amount
                    self.player.deposits += amount

                    system(f'Succesfully deposited ${amount:,.2f}!')
                    system(f'Purse: \x1b[0;97m${self.player.purse:,.2f}')
                    system(f'Deposits: \x1b[0;97m${self.player.deposits:,.2f}')

                elif parts[0] == 'withdraw':
                    if len(parts) != 2:
                        error(f'Command "withdraw" expected '
                              f'1 argument, got {len(parts) - 2}')
                        continue

                    if parts[1] == 'all':
                        amount = self.player.deposits
                    elif parts[1] == 'half':
                        amount = round(self.player.deposits / 2, 2)
                    elif match(r'^\d+('
                               r'(\.\d{0,2})|((\.\d{0,5})?k)'
                               r'|((\.\d{0,8})?m)|((\.\d{0,11})?b)'
                               r'|((\.\d{0,14})?t)'
                               r')?$', parts[1]):
                        if parts[1][-1] in {'k', 'm', 'b', 't'}:
                            amount = float(parts[1][:-1]) * {
                                'k': 1_000,
                                'm': 1_000_000,
                                'b': 1_000_000_000,
                                't': 1_000_000_000_000,
                            }[parts[1][-1]]
                        else:
                            amount = float(parts[1])
                    else:
                        error(f'Invalid amount: {parts[1]}')
                        continue

                    if amount > self.player.deposits:
                        warn('Not enough money in your bank account.')
                        continue

                    self.player.deposits -= amount
                    self.player.purse += amount

                    system(f'Succesfully withdrew ${amount:,.2f}!')
                    system(f'Purse: \x1b[0;97m${self.player.purse:,.2f}')
                    system(f'Deposits: \x1b[0;97m${self.player.deposits:,.2f}')

                elif parts[0] == 'read':
                    if len(parts) == 2:
                        self.inform(parts[1])
                    else:
                        error(f'Command "read" expected at most 1 argument, '
                              f'got {len(parts) - 1}')

                elif parts[0] in {'attr', 'attribute', 'clear', 'exit', 'info',
                                  'information', 'resource', 'save', 'status'}:
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
            system('Successfully saved the game!')
