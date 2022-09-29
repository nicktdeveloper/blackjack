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
        self.num_decks = 6
        self.shoe = shoe.Shoe(self.num_decks)
        self.round_active = True
        self.player_stats = {}
        self.setup_game()

    def setup_game(self):
        """ Function to initialize a game """
        # currently assumes only 1 player will be playing
        # bankroll = int(input('How much money will you be playing with today? '))
        bankroll = 1000
        self.players.append(PlayerModule.Player(bankroll, "Nick"))

        # set up player stats:
        for player in self.players:
            self.player_stats[player.name] = {
                'wins': 0,
                'losses': 0,
                'pushes': 0,
                'games_played': 0
            }

    def setup_round(self):
        """ Function to get the round setup """
        # reset the start of the round
        self.round_active = True
        self.hands = []

    def check_reshuffle(self):
        """ Function to determine if shoe needs to be reshuffled """
        if self.shoe.cards_left() <= self.shoe.cutoff:
            
            self.print_header("Shuffle", "*")
            print(Fore.BLUE + "The shoe will be reshuffled")
            print("")
            self.shoe = shoe.Shoe(self.num_decks)
    
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

        for i, hand in enumerate(self.hands):
            if hand.player.name != "Dealer":
                if not hand.settled_status:
                    self.print_header(f"{hand.player.name.upper()}'s Turn", "+")
                    print(f"{hand.player.name} has {hand.get_hand_value()}")
                    print(f"(Dealer is showing a {self.hands[-1].cards[0].pip_value})")
                    print("")

                    while not hand.stand_status:
                        if hand.check_split():
                            self.player_option_1(hand, i)
                        elif hand.check_doubledown():
                            self.player_option_2(hand)
                        else:
                            self.player_option_3(hand)

                        if hand.check_bust():
                            print(Fore.RED + "This hand has busted!")

                        print("")

                    print(f"{hand.player.name}'s turn has ended.")
    
    def player_option_1(self, hand, idx):
        """ Function if player can split or double """
        answer = input("Hit [1], stand [2], double down [3], or split [4]? ")
        if answer not in ['1', '2', '3', '4']:
            print("Please input a valid response (1, 2, 3, or 4)")
        if answer == '1':
            self.option_hit(hand)
        elif answer == '2':
            self.option_stand(hand)
        elif answer == '3':
            self.option_double(hand)
        elif answer == '4':
            self.option_split(hand, idx)

    def player_option_2(self, hand):
        """ Function if player can double but not split """
        answer = input("Hit [1], stand [2], or double down [3]? ")
        if answer not in ['1', '2', '3']:
            print("Please input a valid response (1, 2, or 3)")
        if answer == '1':
            self.option_hit(hand)
        elif answer == '2':
            self.option_stand(hand)
        elif answer == '3':
            self.option_double(hand)
    
    def player_option_3(self, hand):
        """ Function if player can't split or double """
        answer = input("Hit [1] or stand [2]? ")
        if answer not in ['1', '2']:
            print("Please input a valid response (1 or 2)")
        if answer == '1':
            self.option_hit(hand)
        elif answer == '2':
            self.option_stand(hand)
    
    def option_hit(self, hand):
        """ Function if player decides to hit """
        card_to_hit = self.shoe.deal_card()
        print(f"{hand.player.name} is dealt {card_to_hit.card_name()}")
        hand.hit(card_to_hit)
        print(f"{hand.player.name} has {hand.get_hand_value()}")

    def option_stand(self, hand):
        """ Function if player decides to stand """
        print(f"{hand.player.name} has chosen to stand.")
        hand.stand()

    def option_double(self, hand):
        """ Function if player decides to double """
        card_to_hit = self.shoe.deal_card()
        print(f"{hand.player.name} doubles down (bets additional ${hand.bet})")
        print(f"{hand.player.name} is dealt {card_to_hit.card_name()}")
        hand.double_down(card_to_hit)
        print(f"{hand.player.name} has {hand.get_hand_value()}")

    def option_split(self, hand, idx):
        """ Function if player decides to split """
        print(f"{hand.player.name} elects to split")
        
        # run split function, obtain card to split
        card_to_split = hand.split()

        # initiate new hand, with same bet value
        new_hand = HandModule.Hand(hand.player)
        new_hand.place_bet(hand.bet)
        new_hand.hit(card_to_split)

        # insert the new hand into the hands array
        self.hands.insert(idx + 1, new_hand)
        print(f"{hand.player.name} has {hand.get_hand_value()}")

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
                print(f"{hand.player.name} score is {player_score}")

                # player wins
                if dealer_score > 21 or player_score > dealer_score:
                    print(Fore.GREEN + f'{hand.player.name} wins ${hand.bet}.')
                    hand.player.bankroll += hand.bet * 2
                    self.player_stats[hand.player.name]['wins'] += 1

                # dealer wins
                elif dealer_score > player_score:
                    print(Fore.RED + f'{hand.player.name} loses.')
                    self.player_stats[hand.player.name]['losses'] += 1

                # push
                else:
                    print(Fore.YELLOW + f'{hand.player.name} pushes.')
                    hand.player.bankroll += hand.bet
                    self.player_stats[hand.player.name]['pushes'] += 1

                # change hand status to settled
                hand.settled_status = True

        # mark the round as over
        self.round_active = False

    def stats_readout(self):
        """ Prints out how each player is performing """
        self.print_header("Recap", "-")
        
        # iterate through all players
        for player in self.players:

            stats = self.player_stats[player.name]
            wins = stats['wins']
            losses = stats['losses']
            pushes = stats['pushes']

            # calculate their win %
            try:
                win_pct = stats['wins'] / stats['games_played'] * 100
            except:
                win_pct = 0
            
            # calculate how much they've netted and the %
            net_amt = player.bankroll - player.starting_bankroll
            net_pct = net_amt / player.starting_bankroll * 100

            # print out their stats
            print(f"{player.name}: {wins}-{losses}-{pushes}")
    
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
            self.stats_readout()
            self.play_round()
            self.check_reshuffle()

            print("")
            answer = input("Would you like to continue playing (y/n)? ")

            if answer in ['Y', 'y', 'yes', 'Yes']:
                os.system('clear')
                i += 1
            elif answer in ['N', 'n', 'no', 'No']:
                keep_playing = False

game = Game()
game.play()
