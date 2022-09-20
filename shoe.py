""" Module for shoe objects """
import random
import card

class Shoe:
    """ The shoe class """

    def __init__(self, num_decks: 'int'):
        """ Initialize a single deck card """
        self.cards = []
        self.num_decks = num_decks
        self.cutoff = 0

        # methods to create and shuffle shoe
        self.create_shoe()
        self.shuffle_shoe()
        self.set_cutoff()

    def create_shoe(self):
        """ Method to create a shoe with 52 cards multiplied by num of decks """
        dictionary = {
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "10": 10,
            "J": 10,
            "Q": 10,
            "K": 10,
            "A": 11
        }
        suits = ["clubs", "diamonds", "hearts", "spades"]

        for i in range(self.num_decks):
            for pip, value in dictionary.items():
                for suit in suits:
                    self.cards.append(card.Card(pip, suit, value))

    def cards_left(self):
        """ Returns the number of cards left in the deck """
        return len(self.cards)

    def set_cutoff(self):
        """ Sets a cut off point for when the shoe should be reshuffled """
        self.cutoff = random.randint(60, 75)

    def shuffle_shoe(self):
        """ Shuffles the shoe """
        random.shuffle(self.cards)

    def deal_card(self):
        """ Deals (i.e. pops) one card from the shoe """
        return self.cards.pop()
