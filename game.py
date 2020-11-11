from collections import defaultdict
from time import sleep, time
from os import name, system
from os.path import join
from re import sub


def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


def warn(*args, sep=' ', end='\n'):
    content = sep.join(f'{arg}' for arg in args)
    print(f'\x1b[91m{content}{end}\x1b[0m')


def acknow(*args, sep=' ', end='\n'):
    content = sep.join(f'{arg}' for arg in args)
    print(f'\x1b[96m{content}{end}\x1b[0m')


class Game:
    def __init__(self, assets='assets'):
        self.assets = assets
        self.story = {}
        self.load_story('intro')

        with open(join(self.assets, f'doc.txt')) as file:
            doc = file.read()

        docs = sorted(doc.split('\n\n'),
                      key=lambda part: part.split('\n')[0])
        self.doc = '\n\n'.join(docs)

        cmd_doc = defaultdict(list)

        for doc in docs:
            cmd = doc.split('\n')[0].split()[1]
            cmd_doc[cmd].append(doc)

        self.cmd_doc = {}
        for cmd in cmd_doc:
            self.cmd_doc[cmd] = '\n\n'.join(cmd_doc[cmd])

    def load_story(self, name):
        with open(join(self.assets, 'story', f'{name}.txt')) as file:
            self.story[name] = file.read()

    def inform(self, name):
        if name not in self.story:
            warn(f'Unknown story: "{name}"')
            return

        print(f'===== {name.capitalize()} =====')
        print('Use Ctrl+C to skip.')

        try:
            for ipara, para in enumerate(self.story[name].split('\n\n')):
                sleep(1)
                if ipara > 0:
                    for i in range(2):
                        start = time()
                        print()
                        sleep(max(0, 0.25 - time() + start))
                for char in para:
                    start = time()
                    print(end=char, flush=True)
                    sleep(max(0, 0.05 - time() + start))

            sleep(1)

        except KeyboardInterrupt:
            print()

    def acknow(self, command=''):
        if command == '':
            acknow('Help on commands:')
            acknow(self.doc)
        else:
            if command in self.cmd_doc:
                acknow(f'Help on command "{command}":')
                acknow(self.cmd_doc[command])
            else:
                warn(f'Unknown command: "{command}"')

    def _loop(self):
        while True:
            command = input('> \x1b[1m')
            print(end='\x1b[0m')

            command = sub(r'\s+', command.strip(), r' ')

            if command == 'exit':
                break

            elif command == 'clear':
                clear()

            elif command == 'help':
                self.acknow()

            elif command == 'read':
                warn('Command "read" expected at least 1 argument, got 0')

            elif command:
                parts = command.split()

                if parts[0] == 'help':
                    if len(parts) == 2:
                        self.acknow(parts[1])
                    else:
                        warn(f'Command "help" expected at most 1 argument, '
                             f'got {len(parts) - 1}')

                elif parts[0] == 'read':
                    if len(parts) == 2:
                        self.inform(parts[1])
                    else:
                        warn(f'Command "read" expected at most 1 argument, '
                             f'got {len(parts) - 1}')

                elif parts[0] in {'clear', 'exit'}:
                    warn(f'Command "{parts}" expected no argument, '
                         f'got {len(parts) - 1}')

    def loop(self):
        try:
            self._loop()
        except KeyboardInterrupt:
            print('\x1b[0m')