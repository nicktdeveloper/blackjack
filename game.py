""" Module for game objects and functions """

import os
import math
import colorama
from colorama import Fore
import shoe
import hand as HandModule
import player as PlayerModule

colorama.init(autoreset=True)

class Game:
    """ The game class """

    def __init__(self):
        self.players = []
        self.hands = []
        self.dealer = PlayerModule.Player(1000000, "Dealer")
        self.shoe = shoe.Shoe(6)
        self.round_active = True
        self.setup_game()

    def setup_game(self):
        """ Function to initialize a game """
        # currently assumes only 1 player will be playing

        # bankroll = int(input('How much money will you be playing with today? '))
        bankroll = 1000
        self.players.append(PlayerModule.Player(bankroll, "Nick"))

    def setup_round(self):
        """ Function to get the round setup """
        # reset the start of the round
        self.round_active = True
        self.hands = []

    def deal_cards(self):
        """ Function to deal cards to all players """

        # place bets
        self.print_header("Place Bets", "-")

        bets = {}
        for player in self.players:
            # bet_amt = int(input('How much money would you like to wager? '))
            bet_amount = 10
            print(f"{player.name} bets ${bet_amount}.")
            bets[player] = bet_amount

        # initialize hands for all the players + dealer
        self.print_header("Deal Cards", "-")
        for player in self.players:
            new_hand = HandModule.Hand(player)
            new_hand.place_bet(bets[player])
            self.hands.append(new_hand)

        dealer_hand = HandModule.Hand(self.dealer)
        self.hands.append(dealer_hand)

        # loop through the hands twice, dealing one card each time
        for i in range(2):
            for hand in self.hands:
                card_to_hit = self.shoe.deal_card()
                hand.hit(card_to_hit)

    def insurance(self):
        """ Function to manage when dealer shows ace or 10 card """
        dealer_hand = self.hands[-1]

        # if dealer is showing ace
        if dealer_hand.cards[0].point_value == 11:

            self.print_header("Insurance", "-")
            print("Dealer is showing an Ace")

            # give all players option to purchase insurance
            insurance_bets = {}
            for player in self.players:
                # insurance_bet = int(input('How much insurance would you like to purchase? '))
                insurance_bet = 5
                print(f"{player.name} bets $5 for insurance")
                player.bankroll -= insurance_bet
                insurance_bets[player] = insurance_bet

            # dealer checks if there is natural
            if dealer_hand.check_blackjack():

                print(Fore.RED + "Dealer has blackjack")

                # insurance bets are paid out
                for player in self.players:

                    print(f"{player.name} wins ${insurance_bet * 2} for insurance")
                    player.bankroll += insurance_bets[player] * 2

                # bets are settled
                self.settle_hands()

            else:
                print("Dealer does not have blackjack")
                print("Insurance bets are collected")

        # if dealer is showing face card
        if dealer_hand.cards[0].point_value == 10:
            self.print_header("Dealer Checks for Blackjack", "-")

            print("Dealer is showing a 10 card")

            if dealer_hand.check_blackjack():
                print(Fore.RED + "Dealer has blackjack")

                # bets are settled
                self.settle_hands()

            else:
                print("Dealer does not have blackjack")

    def player_naturals(self):
        """ Function to determine if any players have naturals """
        # don't run the function if it's already over
        if not self.round_active:
            return

        self.print_header("Player Checks for Blackjack", "-")

        any_blackjacks = False

        for hand in self.hands:
            if hand.check_blackjack():
                print(Fore.GREEN + f"{hand.player.name} has blackjack, and wins ${hand.bet * 1.5}!")
                hand.player.bankroll += hand.bet * 2.5
                hand.settled_status = True
                any_blackjacks = True

        if not any_blackjacks:
            print("No players have blackjack")

    def player_turns(self):
        """ Function for all players with active hands to play """
        # don't run the function if it's already over
        if not self.round_active:
            return

        self.print_header("Player Turns", "-")

        for hand in self.hands[:-1]:
            if not hand.settled_status:
                self.print_header(f"{hand.player.name.upper()}'s Turn", "+")
                print(f"{hand.player.name} has {hand.get_hand_value()}")
                print(f"(Dealer is showing a {self.hands[-1].cards[0].pip_value})")
                print("")

                while not hand.stand_status:
                    answer = input("Hit [1] or stand [2]? ")
                    if (answer != '1') and (answer != '2'):
                        print("Please input a valid response (1 or 2)")
                    if answer == '1':
                        card_to_hit = self.shoe.deal_card()
                        print(f"{hand.player.name} is dealt {card_to_hit.card_name()}")
                        hand.hit(card_to_hit)
                        print(f"{hand.player.name} has {hand.get_hand_value()}")
                    elif answer == '2':
                        print(f"{hand.player.name} has chosen to stand.")
                        hand.stand()

                    if hand.check_bust():
                        print(Fore.RED + "This hand has busted!")

                    print("")

                print(f"{hand.player.name}'s turn has ended.")

    def dealers_turn(self):
        """ Function to execute the dealer's turn """
                # don't run the function if it's already over
        if not self.round_active:
            return

        hand = self.hands[-1]

        self.print_header("Dealer's Turn", "-")
        print(f"Dealer reveals a {hand.cards[1].pip_value}")
        print(f"Dealer has {hand.get_hand_value()}")

        if self.check_hands_active():

            print("Beginning dealer's turn.")

            while hand.get_hand_value() < 17:
                card_to_hit = self.shoe.deal_card()
                print("")
                print(f"Dealer is dealt {card_to_hit.card_name()}")
                hand.hit(card_to_hit)
                print(f"{hand.player.name} has {hand.get_hand_value()}")

                if hand.check_bust():
                    print(Fore.GREEN + "Dealer has busted!")

                print("")

        else:
            print("No hands are active")


        print("Dealer's turn has ended.")

    def read_out_cards(self):
        """ Function to read out all player cards """
        for hand in self.hands[:-1]:
            cards_to_readout = []
            for card in hand.cards:
                cards_to_readout.append(card.card_name())

            joined_cards = ' '.join(cards_to_readout)
            print(f'{hand.player.name} has {joined_cards}')

        # reads out dealer's face up card
        dealer_hand = self.hands[-1]
        face_up_card = dealer_hand.cards[0]
        print(f"Dealer is showing a {face_up_card.pip_value}")

    def check_hands_active(self):
        """ Function to determine if any hands are still active """
        for hand in self.hands[:-1]:
            if not hand.settled_status:
                return True
        return False

    def settle_hands(self):
        """ Function to settle bets at the end of the round """
        # don't run the function if it's already over
        if not self.round_active:
            return

        if self.check_hands_active():
            self.print_header("Settling Bets", "-")
            dealer_score = self.hands[-1].get_hand_value()
            print(f"Dealer score is {dealer_score}")

        # loop through all hands but the dealer's hand
        for hand in self.hands[:-1]:
            if not hand.settled_status:
                player_score = hand.get_hand_value()
                print(f"Player score is {player_score}")

                # player wins
                if dealer_score > 21 or player_score > dealer_score:
                    print(Fore.GREEN + f'{hand.player.name} wins ${hand.bet}.')
                    hand.player.bankroll += hand.bet * 2

                # dealer wins
                elif dealer_score > player_score:
                    print(Fore.RED + f'{hand.player.name} loses.')

                # push
                else:
                    print(f'{hand.player.name} pushes.')
                    hand.player.bankroll += hand.bet

                # change hand status to settled
                hand.settled_status = True

        # mark the round as over
        self.round_active = False

    def print_header(self, string, char):
        """ Prints a header with the given string and character """

        total_length = 50
        str_length = len(string)
        remainder = total_length - str_length
        left = math.ceil(remainder / 2) - 1
        right = math.floor(remainder /2) - 1

        output = ""
        output += char * left + " "
        output += string.upper()
        output += " " + char * right

        print("")
        print(output)

    def play_round(self):
        """ Function to play a single round """
        self.setup_round()
        self.deal_cards()
        self.read_out_cards()
        self.insurance()
        self.player_naturals()
        self.player_turns()
        self.dealers_turn()
        self.settle_hands()

    def play(self):
        """ Function to play the game """

        # variable to continue playing
        keep_playing = True
        i = 1

        while keep_playing:
            self.print_header(f"Round {i}", "#")
            self.play_round()

            answer = input("Would you like to continue playing (Y/N)? ")

            if answer == "Y":
                os.system('clear')
                i += 1
            elif answer == "N":
                keep_playing = False

game = Game()
game.play()
