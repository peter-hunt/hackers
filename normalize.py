from os.path import join


def normalize(assets='assets'):
    for path in {'game', 'system'}:
        with open(join(assets, 'doc', f'{path}.txt')) as file:
            doc = sorted(file.read().split('\n\n'),
                         key=lambda part: part.split('\n')[0])
        with open(join(assets, 'doc', f'{path}.txt'), 'w') as file:
            file.write('\n\n'.join(doc))


if __name__ == '__main__':
    normalize()
