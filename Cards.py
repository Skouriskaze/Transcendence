from Transcendence import TranscendenceBoard
from Transcendence import Tile
from enum import Enum
from typing import Set

import random

class CardLevel(Enum):
    NORMAL = 0
    ENHANCED = 1
    MAX = 2


class Card:
    def __init__(self):
        raise NotImplementedError()

    def use(self, board: 'TranscendenceBoard', x: int, y: int) -> Set[tuple]:
        raise NotImplementedError()


class Thunder(Card):
    def __init__(self, level: CardLevel=CardLevel.NORMAL):
        self.level = level
    
    def use(self, board: 'TranscendenceBoard', x: int, y: int) -> Set[tuple]:
        breaks = {
            (0, 0): [1, 1, 1],
            (1, 0): [0.5, 1, 1],
            (0, 1): [0.5, 1, 1],
            (-1, 0): [0.5, 1, 1],
            (0, -1): [0.5, 1, 1],
        }

        hit_tiles = set()
        for (dx, dy), probabilities in breaks.items():
            tile = board.get(x + dx, y + dy)
            if not tile:
                continue
            if not Tile.is_breakable(tile):
                continue
            
            if random.random() < probabilities[self.level.value]:
                if tile is Tile.DISTORTED and self.level is CardLevel.MAX:
                    continue
                else:
                    hit_tiles.add((x + dx, y + dy))

        return hit_tiles

    def __str__(self):
        return 'Thunder'


class Tornado(Card):
    def __init__(self, level: CardLevel=CardLevel.NORMAL):
        self.level = level
    
    def use(self, board: 'TranscendenceBoard', x: int, y: int) -> Set[tuple]:
        breaks = {
            (0, 0): [1, 1, 1],
            (1, 1): [0.5, 1, 1],
            (1, -1): [0.5, 1, 1],
            (-1, 1): [0.5, 1, 1],
            (-1, -1): [0.5, 1, 1],
        }

        hit_tiles = set()
        for (dx, dy), probabilities in breaks.items():
            tile = board.get(x + dx, y + dy)
            if not tile:
                continue
            if not Tile.is_breakable(tile):
                continue
            
            if random.random() < probabilities[self.level.value]:
                if tile is Tile.DISTORTED and self.level is CardLevel.MAX:
                    continue
                else:
                    hit_tiles.add((x + dx, y + dy))

        return hit_tiles

    def __str__(self):
        return 'Tornado'
    

class Purify(Card):
    def __init__(self, level: CardLevel=CardLevel.NORMAL):
        self.level = level
    
    def use(self, board: 'TranscendenceBoard', x: int, y: int) -> Set[tuple]:
        breaks = {
            (0, 0): [1, 1, 1],
            (1, 0): [0.5, 1, 1],
            (-1, 0): [0.5, 1, 1],
            (0, 1): [0, 0, 1],
            (0, -1): [0, 0, 1],
        }

        hit_tiles = set()
        for (dx, dy), probabilities in breaks.items():
            tile = board.get(x + dx, y + dy)
            if not tile:
                continue
            if not Tile.is_breakable(tile):
                continue
            
            if random.random() < probabilities[self.level.value]:
                hit_tiles.add((x + dx, y + dy))

        return hit_tiles

    def __str__(self):
        return 'Purify'
    

class Tempest(Card):
    def __init__(self, level: CardLevel=CardLevel.NORMAL):
        self.level = level

    def use(self, board: 'TranscendenceBoard', x: int, y: int) -> Set[tuple]:
        hit_tiles = set()
        hit_tiles.add((x, y))
        for current_y in range(0, board.height):
            tile = board.get(x, current_y)
            probability = max(0.1, 1 - (0.15 * abs(current_y - y)))
            if random.random() < probability:
                hit_tiles.add((x, current_y))
        return hit_tiles

    def __str__(self):
        return 'Tempest'


class Hellfire(Card):
    def __init__(self, level: CardLevel=CardLevel.NORMAL):
        self.level = level

    def use(self, board: 'TranscendenceBoard', x: int, y: int) -> Set[tuple]:
        raise NotImplementedError()

    def __str__(self):
        return 'Hellfire'


class Shockwave(Card):
    def __init__(self, level: CardLevel=CardLevel.NORMAL):
        self.level = level

    def use(self, board: 'TranscendenceBoard', x: int, y: int) -> Set[tuple]:
        raise NotImplementedError()

    def __str__(self):
        return 'Shockwave'


class Earthquake(Card):
    def __init__(self, level: CardLevel=CardLevel.NORMAL):
        self.level = level

    def use(self, board: 'TranscendenceBoard', x: int, y: int) -> Set[tuple]:
        raise NotImplementedError()

    def __str__(self):
        return 'Earthquake'


class TidalWave(Card):
    def __init__(self, level: CardLevel=CardLevel.NORMAL):
        self.level = level

    def use(self, board: 'TranscendenceBoard', x: int, y: int) -> Set[tuple]:
        raise NotImplementedError()

    def __str__(self):
        return 'Tidal Wave'


class Explosion(Card):
    def __init__(self, level: CardLevel=CardLevel.NORMAL):
        self.level = level

    def use(self, board: 'TranscendenceBoard', x: int, y: int) -> Set[tuple]:
        raise NotImplementedError()

    def __str__(self):
        return 'Explosion'


class Lightning(Card):
    def __init__(self, level: CardLevel=CardLevel.NORMAL):
        self.level = level

    def use(self, board: 'TranscendenceBoard', x: int, y: int) -> Set[tuple]:
        raise NotImplementedError()

    def __str__(self):
        return 'Lightning'
