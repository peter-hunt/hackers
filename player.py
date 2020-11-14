class Player:
    def __init__(self):
        pass

    def dump(self):
        return {}

    @classmethod
    def load(cls, obj):
        return cls()

    @staticmethod
    def is_valid(data):
        if not isinstance(data, dict):
            return False

        return True
