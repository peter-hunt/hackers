from func import error, system


class Player:
    def __init__(self, health=100, hunger=100, purse=0, deposits=0, attr=None):
        self.health = health
        self.hunger = hunger
        self.purse = purse
        self.deposits = deposits

        if attr is None:
            self.attr = {
                # health: have more base health
                'health': 100,
                # regeneration: regenerate sooner and faster,
                #               have bigger stomach
                'regeneration': 100,
                # speed: travel and escape faster
                'speed': 100,
                # strength: deal more damage and carry more weight
                'strength': 100,
                # constitution: be less affected by negative status effects
                'constitution': 100,
                # defense: take less damage from attack
                'defense': 100,
                'intelligence': 100,
                # charisma: buy things for smaller price,
                #           have better NPC reaction
                'charisma': 100,
                # willpower: be less affected by pain, hunger, and fear,
                #            be able to do longer and harder studies
                'willpower': 100,
                # luck: have better luck at all kinds of things
                'luck': 100,
            }
        else:
            self.attr = attr

    def dump(self):
        return {
            'health': self.health,
            'hunger': self.hunger,
            'purse': self.purse,
            'deposits': self.deposits,
            'attr': self.attr,
        }

    @classmethod
    def load(cls, data):
        if not cls.is_valid(data):
            return

        return cls(health=data['health'], hunger=data['hunger'],
                   purse=data['purse'], deposits=data['deposits'],
                   attr=cls.validate_attr(data['attr']))

    @staticmethod
    def is_valid_pos_num(data, key, alert=True):
        if key not in data:
            if alert:
                error(f'Key "{key}" is not found in player data.')
            return False

        value = data[key]

        if not isinstance(value, (int, float)):
            if alert:
                error(f'Player {key} should be an integer or a float, '
                      f'not "{type(value).__name__}".')
            return False

        if value < 0:
            if alert:
                error(f'Player {key} should be non-negative, not "{value}".')
            return False

        return True

    @staticmethod
    def validate_attr(attr, alert=True):
        if not isinstance(attr, dict):
            if alert:
                error(f'Player attribute should be a dicitonary, '
                      f'not "{type(attr).__name__}".')
            return False

        new_attr = {}
        for key in ['health', 'regeneration', 'speed', 'strength',
                    'constitution', 'defense', 'intelligence', 'charisma',
                    'willpower', 'luck']:
            if key not in attr:
                if alert:
                    error(f'Key "{key}" is not found in '
                          f'player attribute data.')

            value = attr[key]

            if not isinstance(value, int):
                if alert:
                    error(f'Player attribute value should be '
                          f'an integer or a float, '
                          f'not "{type(value).__name__}".')
                return False

            if value < 100:
                if alert:
                    error(f'Player attribute value should be '
                          f'at least 100, not "{value}".')
                return False

            new_attr[key] = value

        return new_attr

    @classmethod
    def is_valid(cls, data, *, alert=True):
        if not isinstance(data, dict):
            if alert:
                error(f'Player data should be a dictionary, '
                      f'not "{type(data).__name__}".')
            return False

        for key in {'health', 'hunger', 'purse', 'deposits'}:
            if not cls.is_valid_pos_num(data, key):
                return False

        if 'attr' not in data:
            if alert:
                error('Key "attr" is not found in player data.')
            return False

        if not cls.validate_attr(data['attr']):
            return False

        return True

    def status(self):
        max_health = self.attr['health']
        health = self.health
        _max_health = max_health // 10
        _health = health // 10
        true_health = ' ' * _health
        false_health = ' ' * (_max_health - _health)
        health_perc = 100 * health // max_health

        max_hunger = self.attr['regeneration']
        hunger = self.hunger
        _max_hunger = max_hunger // 10
        _hunger = hunger // 10
        true_hunger = ' ' * _hunger
        false_hunger = ' ' * (_max_hunger - _hunger)
        hunger_perc = 100 * hunger // max_hunger

        system(f'Health  \x1b[0;48;2;232;18;36m{true_health}'
               f'\x1b[100m{false_health}\x1b[0;97m'
               f'  ({health}/{max_health}  {health_perc}%)')
        system(f'Hunger  \x1b[0;48;2;202;80;16m{true_hunger}'
               f'\x1b[100m{false_hunger}\x1b[0;97m'
               f'  ({hunger}/{max_hunger}  {hunger_perc}%)')

    def resource(self):
        system(f'Purse  \x1b[0;97m${self.purse:,.2f}')
        system(f'Deposits  \x1b[0;97m${self.deposits:,.2f}')

    def attribute(self):
        for key in ['health', 'regeneration', 'speed', 'strength',
                    'constitution', 'defense', 'intelligence', 'charisma',
                    'willpower', 'luck']:
            value = self.attr[key]
            value_str = f'{value:,}'
            extra = (value - 100) // 10

            system(f'{key.capitalize():<14}\x1b[90;102m {value_str[:9]:<9}'
                   f'\x1b[106m{value_str[9:]:<{extra}}\x1b[0m')
