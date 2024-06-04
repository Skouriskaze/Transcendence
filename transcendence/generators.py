import random
import cards
import transcendence
from typing import List

class CardGenerator:
    @classmethod
    def get_random_card(cls) -> cards.Card:
        probabilities = {
            cards.Thunder: 150,
            cards.Hellfire: 115,
            cards.Shockwave: 95,
            cards.TidalWave: 55,
            cards.Explosion: 105,
            cards.Tempest: 70,
            cards.Lightning: 90,
            cards.Earthquake: 70,
            cards.Purify: 100,
            cards.Tornado: 150,
        }
        cards = list(probabilities.keys())
        chosen_card = (
            random.choices(cards, [probabilities[card] for card in cards]))
        return chosen_card[0]()

class TileGenerator:
    @classmethod
    def get_random_tile(cls) -> 'transcendence.Tile':
        probabilities = {
            transcendence.Tile.ENHANCEMENT: 160,
            transcendence.Tile.ADDITION: 235,
            transcendence.Tile.CLONE: 160,
            transcendence.Tile.RELOCATION: 0, # normally 170,
            transcendence.Tile.MYSTERY: 160,
            transcendence.Tile.BLESSING: 115,
        }
        tiles = list(probabilities.keys())
        chosen_tile = (
            random.choices(tiles, [probabilities[tile] for tile in tiles]))
        return chosen_tile[0]

class MoveGenerator:
    @classmethod
    def get_valid_moves(cls,
            game: 'transcendence.TranscendenceGame'
        ) -> List['transcendence.TranscendenceMove']:
        # Valid moves are:
        # Changing a card (left or right)
        # Using a card on any breakable tile (left or right)
        # Using a purify on any distorted or breakable tile. Can use level 3? Doubt.
        moves = []
        for x, y in game.board.breakable_tiles:
            left = transcendence.TranscendenceMove(game.hand_left, x, y, True)
            right = transcendence.TranscendenceMove(game.hand_right, x, y, False)
            moves.append(left)
            moves.append(right)
        if game.changes_left > 0:
            left = transcendence.TranscendenceMove(game.hand_left,
                                                   x=None,
                                                   y=None,
                                                   is_left=True,
                                                   is_change=True)
            right = transcendence.TranscendenceMove(game.hand_left,
                                                    x=None,
                                                    y=None,
                                                    is_left=False,
                                                    is_change=True)
            moves.append(left)
            moves.append(right)
        return moves

    @classmethod
    def get_random_move(cls,
            game: 'transcendence.TranscendenceGame'
        ) -> List['transcendence.TranscendenceMove']:
        return random.choice(MoveGenerator.get_valid_moves(game))

