import Transcendence
import Cards
import unittest
import random
from unittest.mock import patch

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


if __name__ == '__main__':
    unittest.main()