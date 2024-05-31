import random
import Cards
import Transcendence
from typing import List

class CardGenerator:
    @classmethod
    def get_random_card(cls) -> Cards.Card:
        probabilities = {
            Cards.Thunder: 150,
            Cards.Hellfire: 115,
            Cards.Shockwave: 95,
            Cards.TidalWave: 55,
            Cards.Explosion: 105,
            Cards.Tempest: 70,
            Cards.Lightning: 90,
            Cards.Earthquake: 70,
            Cards.Purify: 100,
            Cards.Tornado: 150,
        }
        cards = list(probabilities.keys())
        chosen_card = (
            random.choices(cards, [probabilities[card] for card in cards]))
        return chosen_card[0]()

class TileGenerator:
    @classmethod
    def get_random_tile(cls) -> 'Transcendence.Tile':
        probabilities = {
            Transcendence.Tile.ENHANCEMENT: 160,
            Transcendence.Tile.ADDITION: 235,
            Transcendence.Tile.CLONE: 160,
            Transcendence.Tile.RELOCATION: 0, # normally 170,
            Transcendence.Tile.MYSTERY: 160,
            Transcendence.Tile.BLESSING: 115,
        }
        tiles = list(probabilities.keys())
        chosen_tile = (
            random.choices(tiles, [probabilities[tile] for tile in tiles]))
        return chosen_tile[0]

class MoveGenerator:
    @classmethod
    def get_valid_moves(cls,
            game: 'Transcendence.TranscendenceGame'
        ) -> List['Transcendence.TranscendenceMove']:
        # Valid moves are:
        # Changing a card (left or right)
        # Using a card on any breakable tile (left or right)
        # Using a purify on any distorted or breakable tile. Can use level 3? Doubt.
        moves = []
        for x, y in game.board.breakable_tiles:
            left = Transcendence.TranscendenceMove(game.hand_left, x, y, True)
            right = Transcendence.TranscendenceMove(game.hand_right, x, y, False)
            moves.append(left)
            moves.append(right)
        if game.changes_left > 0:
            left = Transcendence.TranscendenceMove(game.hand_left,
                                                   x=None,
                                                   y=None,
                                                   is_left=True,
                                                   is_change=True)
            right = Transcendence.TranscendenceMove(game.hand_left,
                                                    x=None,
                                                    y=None,
                                                    is_left=False,
                                                    is_change=True)
            moves.append(left)
            moves.append(right)
        return moves

    @classmethod
    def get_random_move(cls,
            game: 'Transcendence.TranscendenceGame'
        ) -> List['Transcendence.TranscendenceMove']:
        return random.choice(MoveGenerator.get_valid_moves(game))

