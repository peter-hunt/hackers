from collections import defaultdict
from time import sleep, time
from os.path import join
from re import sub

from __init__ import __version__
from func import clear, error, warn, acknow


class System:
    def __init__(self, assets='assets'):
        # load the assets
        self.assets = assets

        with open(join(self.assets, 'doc', 'system.txt')) as file:
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

        with open(join(self.assets, 'warnings.txt')) as file:
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
                    sleep(1)

                    if ipara > 1:
                        for _ in range(2):
                            start = time()
                            warn()
                            sleep(max(0, 0.1 - time() + start))

                    for char in para:
                        start = time()
                        warn(end=char, flush=True)
                        sleep(max(0, 0.02 - time() + start))

            sleep(1)

            start = time()
            warn()
            sleep(max(0, 0.1 - time() + start))

            sleep(3)

        except KeyboardInterrupt:
            print(end='\x1b[0m')

    def _loop(self):
        acknow(f'Hackers {__version__}')
        acknow('Type "help" for more information.')

        while True:
            command = input('> \x1b[1m')
            print(end='\x1b[0m')

            command = sub(r'\s+', command, r' ').strip()

            if command == 'exit':
                break

            elif command == 'clear':
                clear()

            elif command == 'help':
                self.acknow()

            elif command:
                parts = command.split()

                if parts[0] == 'help':
                    if len(parts) == 2:
                        self.acknow(parts[1])
                    else:
                        error(f'Command "help" expected at most 1 argument, '
                              f'got {len(parts) - 1}')

                elif parts[0] in {'clear', 'exit'}:
                    error(f'Command "{parts[0]}" expected no argument, '
                          f'got {len(parts) - 1}')

                else:
                    error(f'Unknown command: "{parts[0]}"')

    def loop(self):
        clear()

        self.warn()

        clear()

        try:
            self._loop()
        except KeyboardInterrupt:
            print('\x1b[0m')
