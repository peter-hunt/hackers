from json import dump, load
from json.decoder import JSONDecodeError
from os import walk
from os.path import join
from re import match


def normalize():
    for path in {'game', 'system'}:
        with open(join('assets', 'doc', f'{path}.txt')) as file:
            doc = sorted(file.read().split('\n\n'),
                         key=lambda part: part.split('\n')[0])
        with open(join('assets', 'doc', f'{path}.txt'), 'w') as file:
            file.write('\n\n'.join(doc))

    for path in next(walk('saves'))[2]:
        if not match(r'^\S+\.json$', path):
            continue

        try:
            with open(join('saves', path)) as file:
                data = load(file)
        except JSONDecodeError:
            continue

        with open(join('saves', path), 'w') as file:
            dump(data, file, indent=2, sort_keys=True)


if __name__ == '__main__':
    normalize()
