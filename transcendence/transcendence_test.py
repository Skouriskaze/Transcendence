import random
import unittest

from . import transcendence
from . import cards
from . import generators

from unittest.mock import patch, Mock

# Tests to add:

# TODO: Test for each tile.
class TestTileEnhancements(unittest.TestCase):
    def setUp(self):
        self.board = transcendence.TranscendenceBoard(5, 5)
        self.game = transcendence.TranscendenceGame(self.board)
        self.move_left = transcendence.TranscendenceMove(self.game.hand_left, 1, 1, True)
        self.move_right = transcendence.TranscendenceMove(self.game.hand_right, 1, 1, False)

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
    @patch('transcendence.random')
    def test_mystery_tree_left(self, random):
        random.choice.return_value = True
        self.game.mystery(self.move_left)
        self.assertIsInstance(self.game.hand_right, cards.Tree)

    @patch('transcendence.random')
    def test_mystery_outburst_left(self, random):
        random.choice.return_value = False
        self.game.mystery(self.move_left)
        self.assertIsInstance(self.game.hand_right, cards.Outburst)

    @patch('transcendence.random')
    def test_mystery_tree_right(self, random):
        random.choice.return_value = True
        self.game.mystery(self.move_right)
        self.assertIsInstance(self.game.hand_left, cards.Tree)

    @patch('transcendence.random')
    def test_mystery_outburst_right(self, random):
        random.choice.return_value = False
        self.game.mystery(self.move_right)
        self.assertIsInstance(self.game.hand_left, cards.Outburst)

    # ----- Enhancement Tiles -----
    def test_enhancement_left(self):
        base_level = 1
        self.game.hand_right.level = cards.CardLevel(base_level)
        self.game.enhance(self.move_left)
        target = cards.CardLevel(base_level + 1)
        self.assertEqual(target, self.game.hand_right.level)

    def test_enhancement_right(self):
        base_level = 1
        self.game.hand_left.level = cards.CardLevel(base_level)
        self.game.enhance(self.move_right)
        target = cards.CardLevel(base_level + 1)
        self.assertEqual(target, self.game.hand_left.level)

    def test_enhancement_max_left(self):
        self.game.hand_right.level = cards.CardLevel.MAX
        self.game.enhance(self.move_left)
        self.assertEqual(cards.CardLevel.MAX, self.game.hand_right.level)

    def test_enhancement_max_right(self):
        self.game.hand_left.level = cards.CardLevel.MAX
        self.game.enhance(self.move_right)
        self.assertEqual(cards.CardLevel.MAX, self.game.hand_left.level)


class TestCards(unittest.TestCase):
    def setUp(self) -> None:
        board = transcendence.TranscendenceBoard(5, 5)
        game = transcendence.TranscendenceGame(board)
        game.hand_left = cards.Thunder()
        game.hand_right = cards.Thunder()
        game.hand_queue = (
            [cards.Lightning(), cards.Tempest(), cards.Earthquake()]
        )
        self.game = game

    def test_card_folding(self):
        generators.CardGenerator.get_random_card = Mock()
        generators.CardGenerator.get_random_card.side_effect = (
            [cards.Shockwave(), cards.Tornado(), cards.Hellfire()]
        )
        self.game.fix_hand()
        self.assertEqual(self.game.hand_left, cards.Thunder(cards.CardLevel.ENHANCED))
        self.assertEqual(self.game.hand_right, cards.Lightning())
        self.assertListEqual(self.game.hand_queue, [cards.Tempest(), cards.Earthquake(), cards.Shockwave()])

    def test_card_folding_twice(self):
        generators.CardGenerator.get_random_card = Mock()
        generators.CardGenerator.get_random_card.side_effect = (
            [cards.Shockwave(), cards.Tornado(), cards.Hellfire()]
        )
        self.game.hand_queue[0] = cards.Thunder()
        self.game.fix_hand()
        self.assertEqual(self.game.hand_left, cards.Thunder(cards.CardLevel.MAX))
        self.assertEqual(self.game.hand_right, cards.Tempest())
        self.assertListEqual(self.game.hand_queue, [cards.Earthquake(), cards.Shockwave(), cards.Tornado()])

if __name__ == '__main__':
    unittest.main()