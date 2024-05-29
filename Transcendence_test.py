import Transcendence
import Cards
import unittest
import Generators
import random
from unittest.mock import patch, Mock

# Tests to add:

# TODO: Test for each tile.
class TestTileEnhancements(unittest.TestCase):
    def setUp(self):
        self.board = Transcendence.TranscendenceBoard(5, 5)
        self.game = Transcendence.TranscendenceGame(self.board)
        self.move_left = Transcendence.TranscendenceMove(self.game.hand_left, 1, 1, True)
        self.move_right = Transcendence.TranscendenceMove(self.game.hand_right, 1, 1, False)

    # ----- Bless Tiles -----
    def test_bless(self):
        base_turns = self.game.turns_left
        self.game.bless(self.move_left)
        self.assertEqual(base_turns + 1, self.game.turns_left)
        
    # ----- Addition Tiles -----
    def test_addition(self):
        base_changes = self.game.changes_left
        self.game.add(self.move_left)
        self.assertEqual(base_changes + 1, self.game.changes_left)
    
    # ----- Clone Tiles -----
    def test_clone_left(self):
        self.game.clone(self.move_left)
        self.assertEqual(self.game.hand_right, self.move_left.card)

    def test_clone_right(self):
        self.game.clone(self.move_right)
        self.assertEqual(self.game.hand_left, self.move_right.card)

    # ----- Mystery Tiles -----
    @patch('Transcendence.random')
    def test_mystery_tree_left(self, random):
        random.choice.return_value = True
        self.game.mystery(self.move_left)
        self.assertIsInstance(self.game.hand_right, Cards.Tree)

    @patch('Transcendence.random')
    def test_mystery_outburst_left(self, random):
        random.choice.return_value = False
        self.game.mystery(self.move_left)
        self.assertIsInstance(self.game.hand_right, Cards.Outburst)

    @patch('Transcendence.random')
    def test_mystery_tree_right(self, random):
        random.choice.return_value = True
        self.game.mystery(self.move_right)
        self.assertIsInstance(self.game.hand_left, Cards.Tree)

    @patch('Transcendence.random')
    def test_mystery_outburst_right(self, random):
        random.choice.return_value = False
        self.game.mystery(self.move_right)
        self.assertIsInstance(self.game.hand_left, Cards.Outburst)

    # ----- Enhancement Tiles -----
    def test_enhancement_left(self):
        base_level = 1
        self.game.hand_right.level = Cards.CardLevel(base_level)
        self.game.enhance(self.move_left)
        target = Cards.CardLevel(base_level + 1)
        self.assertEqual(target, self.game.hand_right.level)

    def test_enhancement_right(self):
        base_level = 1
        self.game.hand_left.level = Cards.CardLevel(base_level)
        self.game.enhance(self.move_right)
        target = Cards.CardLevel(base_level + 1)
        self.assertEqual(target, self.game.hand_left.level)

    def test_enhancement_max_left(self):
        self.game.hand_right.level = Cards.CardLevel.MAX
        self.game.enhance(self.move_left)
        self.assertEqual(Cards.CardLevel.MAX, self.game.hand_right.level)

    def test_enhancement_max_right(self):
        self.game.hand_left.level = Cards.CardLevel.MAX
        self.game.enhance(self.move_right)
        self.assertEqual(Cards.CardLevel.MAX, self.game.hand_left.level)


class TestCards(unittest.TestCase):
    def setUp(self) -> None:
        board = Transcendence.TranscendenceBoard(5, 5)
        game = Transcendence.TranscendenceGame(board)
        game.hand_left = Cards.Thunder()
        game.hand_right = Cards.Thunder()
        game.hand_queue = (
            [Cards.Lightning(), Cards.Tempest(), Cards.Earthquake()]
        )
        self.game = game

    def test_card_folding(self):
        Generators.CardGenerator.get_random_card = Mock()
        Generators.CardGenerator.get_random_card.side_effect = (
            [Cards.Shockwave(), Cards.Tornado(), Cards.Hellfire()]
        )
        self.game.fix_hand()
        self.assertEqual(self.game.hand_left, Cards.Thunder(Cards.CardLevel.ENHANCED))
        self.assertEqual(self.game.hand_right, Cards.Lightning())
        self.assertListEqual(self.game.hand_queue, [Cards.Tempest(), Cards.Earthquake(), Cards.Shockwave()])

    def test_card_folding_twice(self):
        Generators.CardGenerator.get_random_card = Mock()
        Generators.CardGenerator.get_random_card.side_effect = (
            [Cards.Shockwave(), Cards.Tornado(), Cards.Hellfire()]
        )
        self.game.hand_queue[0] = Cards.Thunder()
        self.game.fix_hand()
        self.assertEqual(self.game.hand_left, Cards.Thunder(Cards.CardLevel.MAX))
        self.assertEqual(self.game.hand_right, Cards.Tempest())
        self.assertListEqual(self.game.hand_queue, [Cards.Earthquake(), Cards.Shockwave(), Cards.Tornado()])

if __name__ == '__main__':
    unittest.main()