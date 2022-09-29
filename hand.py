""" Module for hand objects """
# import card

class Hand:
    """ The hand class """

    def __init__(self, player):
        self.cards = []
        self.value = 0
        self.bet = 0
        self.player = player
        self.bust_status = False
        self.split_status = False
        self.stand_status = False
        self.settled_status = False

    def place_bet(self, amt):
        """ Adds money to the hand """
        self.player.bankroll -= amt
        self.bet += amt

    def hit(self, card):
        """ Adds one card to the hand """
        self.cards.append(card)

        # recalculates the hands value after every hit
        self.calc_value()

    def double_down(self, card):
        """ Doubles bet, adds one card to the hand """

        # currently assumes that player has sufficient money
        # need to add check to ensure player has enough money to bet

        self.place_bet(self.bet)
        self.hit(card)
        self.stand()

    def split(self):
        """ Splits the hand if cards are of matching pip value """
        # Returns the card to be added to the new hand
        card_to_split = self.cards.pop()

        # recalculates the hands value after splitting
        self.calc_value()

        return card_to_split


    def stand(self):
        """ Changes stand status to true """
        self.stand_status = True

    def calc_value(self):
        """ Calculates the best possible value of the hand """
        total = 0

        # separate aces and non-aces into two lists, count number of aces
        non_aces_values = [card.point_value for card in self.cards if card.point_value < 11]
        aces_values = [card.point_value for card in self.cards if card.point_value == 11]
        num_aces = len(aces_values)

        # sum up all non-aces
        total = sum(non_aces_values)
        self.value = total

        if num_aces > 0:
            total_max = total + num_aces + 10
            total_min = total + num_aces

            if total_max <= 21:
                self.value = total_max
            else:
                self.value = total_min

    def get_hand_value(self):
        """ Returns the hands value """
        return self.value

    def check_bust(self):
        """ Checks whether the hand has busted """
        if self.value > 21:
            self.stand_status = True
            self.settled_status = True
            return True
        else:
            return False

    def check_doubledown(self):
        """ Checks whether the hand can double down """
        return len(self.cards) == 2

    def check_split(self):
        """ Checks if the hand can be split """
        return (len(self.cards) == 2) and (self.cards[0].pip_value == self.cards[1].pip_value)

    def check_blackjack(self):
        """ Check whether the hand is a natural blackjack """
        return len(self.cards) == 2 and self.value == 21
