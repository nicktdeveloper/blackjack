""" Testing for all Blackjack modules """
import unittest
# from unittest.mock import patch
import card
import shoe
import hand
import player

class TestEmployee(unittest.TestCase):
    """ Main testing class """
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.card1 = card.Card('A', 'spades', 11)
        self.card2 = card.Card('K', 'clubs', 10)
        self.card3 = card.Card('A', 'hearts', 11)
        self.card4 = card.Card('7', 'diamonds', 7)

        self.shoe1 = shoe.Shoe(1)
        self.shoe2 = shoe.Shoe(2)
        self.shoe3 = shoe.Shoe(6)

        self.player1 = player.Player(1000, "Andy")
        self.player2 = player.Player(500, "Bob")
        self.player3 = player.Player(2500, "Cat")

        self.hand1 = hand.Hand(self.player1)
        self.hand1.place_bet(5)
        self.hand1.hit(self.card1)
        self.hand1.hit(self.card2)

        self.hand2 = hand.Hand(self.player2)
        self.hand2.place_bet(10)
        self.hand2.hit(self.card1)
        self.hand2.hit(self.card2)
        self.hand2.hit(self.card3)

        self.hand3 = hand.Hand(self.player3)
        self.hand3.place_bet(15)
        self.hand3.hit(self.card1)
        self.hand3.hit(self.card3)
        self.hand3.hit(self.card4)

        self.hand4 = hand.Hand(self.player1)
        self.hand4.place_bet(20)
        self.hand4.hit(self.card2)
        self.hand4.hit(self.card2)
        self.hand4.hit(self.card3)
        self.hand4.hit(self.card4)

        self.hand5 = hand.Hand(self.player1)
        self.hand5.place_bet(20)
        self.hand5.hit(self.card1)
        self.hand5.hit(self.card3)

    def tearDown(self):
        pass

    def test_pip_value(self):
        """ Method to test whether card pip value is returned correctly """
        self.assertEqual(self.card1.card_name(), 'As')
        self.assertEqual(self.card2.card_name(), 'Kc')
        self.assertEqual(self.card3.card_name(), 'Ah')
        self.assertEqual(self.card4.card_name(), '7d')

    def test_shoe_size(self):
        """ Method to test whether shoe has the correct amount of starting cards """
        self.assertEqual(self.shoe1.cards_left(), 52)
        self.assertEqual(self.shoe2.cards_left(), 104)
        self.assertEqual(self.shoe3.cards_left(), 312)

    def test_shoe_cutoff(self):
        """ Test whether cut off point is between 60 and 75 """
        self.assertGreaterEqual(self.shoe1.cutoff, 60)
        self.assertLessEqual(self.shoe1.cutoff, 75)
        self.assertGreaterEqual(self.shoe2.cutoff, 60)
        self.assertLessEqual(self.shoe2.cutoff, 75)
        self.assertGreaterEqual(self.shoe3.cutoff, 60)
        self.assertLessEqual(self.shoe3.cutoff, 75)

    def test_shoe_shuffle(self):
        """ Test whether shoe shuffle works correctly """
        preshuffle1 = self.shoe1.cards.copy()
        self.shoe1.shuffle_shoe()
        postshuffle1 = self.shoe1.cards.copy()
        preshuffle2 = self.shoe2.cards.copy()
        self.shoe2.shuffle_shoe()
        postshuffle2 = self.shoe2.cards.copy()

        self.assertNotEqual(preshuffle1, postshuffle1)
        self.assertNotEqual(preshuffle2, postshuffle2)

    def test_shoe_deal_card(self):
        """ Test whether card is dealt correctly from shoe """
        precount1 = self.shoe1.cards_left()
        self.shoe1.deal_card()
        precount2 = self.shoe2.cards_left()
        self.shoe2.deal_card()

        self.assertEqual(precount1, self.shoe1.cards_left() + 1)
        self.assertEqual(precount2, self.shoe2.cards_left() + 1)

    def test_hand_calc_value(self):
        """ Test whether hand values are calculated correctly """
        self.assertEqual(self.hand1.get_hand_value(), 21)
        self.assertEqual(self.hand2.get_hand_value(), 12)
        self.assertEqual(self.hand3.get_hand_value(), 19)
        self.assertEqual(self.hand4.get_hand_value(), 28)

    def test_hand_place_bet(self):
        """ Test whether the place bet function works """
        self.assertEqual(self.hand1.bet, 5)
        self.assertEqual(self.hand2.bet, 10)
        self.assertEqual(self.hand3.bet, 15)

        # test double down function
        self.hand1.double_down(self.card4)
        self.assertEqual(self.hand1.bet, 10)

    def test_hand_check_bust(self):
        """ Tests whether the bust check function works """
        self.assertFalse(self.hand1.check_bust())
        self.assertFalse(self.hand2.check_bust())
        self.assertFalse(self.hand3.check_bust())
        self.assertTrue(self.hand4.check_bust())

    def test_hand_check_blackjack(self):
        """ Test whether the check blackjack function works """
        self.assertTrue(self.hand1.check_blackjack())
        self.assertFalse(self.hand2.check_blackjack())
        self.assertFalse(self.hand3.check_blackjack())
        self.assertFalse(self.hand4.check_blackjack())

    def test_hand_check_split(self):
        """ Test whether the check split function works """
        self.assertFalse(self.hand1.check_split())
        self.assertFalse(self.hand2.check_split())
        self.assertFalse(self.hand3.check_split())
        self.assertFalse(self.hand4.check_split())
        self.assertTrue(self.hand5.check_split())

    def test_hand_split(self):
        """ Test whether the split function works """
        self.assertEqual(self.hand5.split(), self.card3)
        self.assertEqual(self.hand5.cards[0], self.card1)

    def test_game_deal(self):
        """ Test to ensure deal function works properly """
        pass

if __name__ == '__main__':
    unittest.main()
