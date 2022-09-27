""" Module for player objects """

class Player:
    """ The player class """

    def __init__(self, bankroll: 'int', name: 'str'):
        self.starting_bankroll = bankroll
        self.bankroll = bankroll
        self.name = name
