""" Module for card objects """

class Card:
    """ The card class """

    def __init__(self, pip_value: 'str', suit: 'str', point_value: 'int'):
        """ Initialize an individual card """
        self.pip_value = pip_value
        self.suit = suit
        self.point_value = point_value

    def card_name(self):
        """ Returns the card pip value and its suit """
        return self.pip_value + self.suit[0]
