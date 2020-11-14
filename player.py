from func import error, acknow


class Player:
    def __init__(self, purse=0, deposits=0):
        self.purse = purse
        self.deposits = deposits

    def dump(self):
        return {
            'purse': self.purse,
            'deposits': self.deposits,
        }

    @classmethod
    def load(cls, data):
        if not cls.is_valid(data):
            return

        return cls(purse=data['purse'], deposits=data['deposits'])

    @staticmethod
    def is_valid(data, *, alert=True):
        if not isinstance(data, dict):
            if alert:
                error(f'Player data should be a dictionary, '
                      f'not "{type(data).__name__}".')
            return False

        if 'purse' not in data:
            if alert:
                error('Key "purse" is not found in player data.')
            return False

        purse = data['purse']

        if not isinstance(purse, (int, float)):
            if alert:
                error(f'Player purse should be an integer or a float, '
                      f'not "{type(purse).__name__}".')
            return False

        if purse < 0:
            if alert:
                error(f'Player purse should be non-negative, not "{purse}".')
            return False

        if 'deposits' not in data:
            if alert:
                error('Key "deposits" is not found in player data.')
            return False

        deposits = data['deposits']

        if not isinstance(deposits, (int, float)):
            if alert:
                error(f'Player deposits should be an integer or a float, '
                      f'not "{type(deposits).__name__}".')
            return False

        if deposits < 0:
            if alert:
                error(f'Player deposits should be non-negative, '
                      f'not "{deposits}".')
            return False

        return True

    def info(self):
        acknow(f'Purse: {self.purse:,.2f}$')

    def information(self):
        acknow(f'Purse: {self.purse:,.2f}$')
        acknow(f'Deposits: {self.deposits:,.2f}$')
