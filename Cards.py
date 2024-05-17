from Transcendence import TranscendenceBoard
from Transcendence import TranscendenceGame
from enum import Enum
from typing import List

class CardLevel(Enum):
    NORMAL = 0
    ENHANCED = 1
    MAX = 2


class Card:
    def __init__(self):
        raise NotImplementedError()

    def use(self, board: 'TranscendenceBoard') -> List[tuple]:
        raise NotImplementedError()


class Thunder(Card):
    def __init__(self, level: CardLevel=CardLevel.NORMAL):
        self.level = level
    
    def use(self, board: 'TranscendenceBoard', x: int, y: int) -> List[tuple]:
        breaks = {
            (0, 0): [1, 1, 1],
            (1, 0): [0.5, 1, 1],
            (0, 1): [0.5, 1, 1],
            (-1, 0): [0.5, 1, 1],
            (0, -1): [0.5, 1, 1],
        }

        hit_tiles = []
        for (dx, dy), probabilities in breaks.items():
            tile = board.get(x + dx, y + dy)
            if not tile:
                continue
            if tile is Tile.DESTROYED:
                continue
            
            if random.random() < probabilities[self.level.value]:
                if tile is Tile.DISTORTED and self.level is CardLevel.MAX:
                    continue
                else:
                    hit_tiles.append((x + dx, y + dy))

        return hit_tiles

    def __str__(self):
        return 'Thunder'


class Tornado(Card):
    def __init__(self, level: CardLevel=CardLevel.NORMAL):
        self.level = level
    
    def use(self, board: 'TranscendenceBoard', x: int, y: int) -> List[tuple]:
        breaks = {
            (0, 0): [1, 1, 1],
            (1, 1): [0.5, 1, 1],
            (1, -1): [0.5, 1, 1],
            (-1, 1): [0.5, 1, 1],
            (-1, -1): [0.5, 1, 1],
        }

        hit_tiles = []
        for (dx, dy), probabilities in breaks.items():
            tile = board.get(x + dx, y + dy)
            if not tile:
                continue
            if tile is Tile.DESTROYED:
                continue
            
            if random.random() < probabilities[self.level.value]:
                if tile is Tile.DISTORTED and self.level is CardLevel.MAX:
                    continue
                else:
                    hit_tiles.append((x + dx, y + dy))

        return hit_tiles

    def __str__(self):
        return 'Tornado'
    

class Purify(Card):
    def __init__(self, level: CardLevel=CardLevel.NORMAL):
        self.level = level
    
    def use(self, board: 'TranscendenceBoard', x: int, y: int) -> List[tuple]:
        breaks = {
            (0, 0): [1, 1, 1],
            (1, 0): [0.5, 1, 1],
            (-1, 0): [0.5, 1, 1],
            (0, 1): [0, 0, 1],
            (0, -1): [0, 0, 1],
        }

        hit_tiles = []
        for (dx, dy), probabilities in breaks.items():
            tile = board.get(x + dx, y + dy)
            if not tile:
                continue
            if not Tile.is_breakable(tile):
                continue
            
            if random.random() < probabilities[self.level.value]:
                hit_tiles.append((x + dx, y + dy))

        return hit_tiles

    def __str__(self):
        return 'Tornado'
    
