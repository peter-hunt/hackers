from func import error


class Npc:
    def __init__(self, npcs=None):
        if npcs is None:
            self.npcs = []
        else:
            self.npcs = npcs

    def dump(self):
        return sorted(self.npcs, key=lambda npc: npc['id'])

    @classmethod
    def load(cls, data):
        if not cls.is_valid(data):
            return

        return cls(npcs=data)

    @staticmethod
    def is_valid(data, *, alert=True):
        if not isinstance(data, list):
            if alert:
                error(f'Npc data should be a list, '
                      f'not "{type(data).__name__}".')
            return False

        for npc in data:
            if 'name' not in npc:
                if alert:
                    error('Key "name" is not found in npc data.')
                return False

            name = npc['name']

            if not isinstance(name, str):
                if alert:
                    error(f'Npc name should be a string, '
                          f'not "{type(name).__name__}".')
                return False

            if 'id' not in npc:
                if alert:
                    error('Key "id" is not found in npc data.')
                return False

            id = npc['id']

            if not isinstance(id, str):
                if alert:
                    error(f'Npc id should be an integer, '
                          f'not "{type(id).__name__}".')
                return False

            if id < 0:
                if alert:
                    error(f'Npc id should be a non-negative integer, '
                          f'not {id}.')
                return False

        return True
