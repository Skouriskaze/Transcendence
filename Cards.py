from enum import Enum
from typing import Set
from typing import Dict
from typing import Tuple
from typing import List

import Transcendence
import random

class CardLevel(Enum):
    NORMAL = 0
    ENHANCED = 1
    MAX = 2


class Card:
    def __init__(self):
        raise NotImplementedError()

    def use(self, board: 'Transcendence.TranscendenceBoard', x: int, y: int) -> Set[tuple]:
        raise NotImplementedError()

    @classmethod
    def get_hit_tiles(self,
                      board: 'Transcendence.TranscendenceBoard',
                      x: int,
                      y: int,
                      breaks: Dict[Tuple, List]) -> Set[Tuple]:
        hit_tiles = set()
        for (dx, dy), probabilities in breaks.items():
            tile = board.get(x + dx, y + dy)
            if not tile:
                continue
            if not Transcendence.Tile.is_breakable(tile):
                continue
            
            if random.random() < probabilities[self.level.value]:
                if tile is Transcendence.Tile.DISTORTED and self.level is CardLevel.MAX:
                    continue
                else:
                    hit_tiles.add((x + dx, y + dy))

        return hit_tiles

class Thunder(Card):
    def __init__(self, level: CardLevel=CardLevel.NORMAL):
        self.level = level
    
    def use(self, board: 'Transcendence.TranscendenceBoard', x: int, y: int) -> Set[tuple]:
        breaks = {
            (0, 0): [1, 1, 1],
            (1, 0): [0.5, 1, 1],
            (0, 1): [0.5, 1, 1],
            (-1, 0): [0.5, 1, 1],
            (0, -1): [0.5, 1, 1],
        }

        return Card.get_hit_tiles(board, x, y, breaks)

    def __str__(self):
        return 'Thunder'


class Tornado(Card):
    def __init__(self, level: CardLevel=CardLevel.NORMAL):
        self.level = level
    
    def use(self, board: 'Transcendence.TranscendenceBoard', x: int, y: int) -> Set[tuple]:
        breaks = {
            (0, 0): [1, 1, 1],
            (1, 1): [0.5, 1, 1],
            (1, -1): [0.5, 1, 1],
            (-1, 1): [0.5, 1, 1],
            (-1, -1): [0.5, 1, 1],
        }

        return Card.get_hit_tiles(board, x, y, breaks)

    def __str__(self):
        return 'Tornado'
    

class Purify(Card):
    def __init__(self, level: CardLevel=CardLevel.NORMAL):
        self.level = level
    
    def use(self, board: 'Transcendence.TranscendenceBoard', x: int, y: int) -> Set[tuple]:
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
            if not Transcendence.Tile.is_breakable(tile):
                continue
            
            if random.random() < probabilities[self.level.value]:
                hit_tiles.add((x + dx, y + dy))

        return hit_tiles

    def __str__(self):
        return 'Purify'
    

class Tempest(Card):
    def __init__(self, level: CardLevel=CardLevel.NORMAL):
        self.level = level

    def use(self, board: 'Transcendence.TranscendenceBoard', x: int, y: int) -> Set[tuple]:
        hit_tiles = set()
        for current_y in range(0, board.height):
            tile = board.get(x, current_y)
            if not Transcendence.Tile.is_breakable(tile):
                continue

            probability = max(0.1, 1 - (0.15 * abs(current_y - y)))
            if random.random() < probability:
                hit_tiles.add((x, current_y))

        return hit_tiles

    def __str__(self):
        return 'Tempest'


class Hellfire(Card):
    def __init__(self, level: CardLevel=CardLevel.NORMAL):
        self.level = level

    def use(self, board: 'Transcendence.TranscendenceBoard', x: int, y: int) -> Set[tuple]:
        breaks = {
            (0, 0): [1, 1, 1],
        }
        for x in range(4):
            for y in range(4 - x):
                if x == 0 and y == 0:
                    continue
                breaks[(x, y)] = [0.5, 1, 1]
                breaks[(-x, y)] = [0.5, 1, 1]
                breaks[(x, -y)] = [0.5, 1, 1]
                breaks[(-x, -y)] = [0.5, 1, 1]

        return Card.get_hit_tiles(board, x, y, breaks)

    def __str__(self):
        return 'Hellfire'


class Shockwave(Card):
    def __init__(self, level: CardLevel=CardLevel.NORMAL):
        self.level = level

    def use(self, board: 'Transcendence.TranscendenceBoard', x: int, y: int) -> Set[tuple]:
        breaks = {
            (0, 0): [1, 1, 1],
            (1, -1): [0.75, 1, 1],
            (1, 0): [0.75, 1, 1],
            (1, 1): [0.75, 1, 1],
            (0, -1): [0.75, 1, 1],
            (0, 1): [0.75, 1, 1],
            (1, -1): [0.75, 1, 1],
            (1, 0): [0.75, 1, 1],
            (1, 1): [0.75, 1, 1],
        }
        return Card.get_hit_tiles(board, x, y, breaks)

    def __str__(self):
        return 'Shockwave'


class Earthquake(Card):
    def __init__(self, level: CardLevel=CardLevel.NORMAL):
        self.level = level

    def use(self, board: 'Transcendence.TranscendenceBoard', x: int, y: int) -> Set[tuple]:
        hit_tiles = set()
        for current_x in range(0, board.width):
            tile = board.get(current_x, y)
            if not Transcendence.Tile.is_breakable(tile):
                continue

            probability = max(0.1, 1 - (0.15 * abs(current_x - x)))
            if random.random() < probability:
                hit_tiles.add((current_x, y))

        return hit_tiles

    def __str__(self):
        return 'Earthquake'


class TidalWave(Card):
    def __init__(self, level: CardLevel=CardLevel.NORMAL):
        self.level = level

    def use(self, board: 'Transcendence.TranscendenceBoard', x: int, y: int) -> Set[tuple]:
        hit_tiles = set()
        for current_x in range(0, board.width):
            tile = board.get(current_x, y)
            if not Transcendence.Tile.is_breakable(tile):
                continue

            probability = max(0.1, 1 - (0.15 * abs(current_x - x)))
            if random.random() < probability:
                hit_tiles.add((current_x, y))

        for current_y in range(0, board.height):
            tile = board.get(x, current_y)
            if not Transcendence.Tile.is_breakable(tile):
                continue

            probability = max(0.1, 1 - (0.15 * abs(current_y - y)))
            if random.random() < probability:
                hit_tiles.add((x, current_y))

        return hit_tiles

    def __str__(self):
        return 'Tidal Wave'


class Explosion(Card):
    def __init__(self, level: CardLevel=CardLevel.NORMAL):
        self.level = level

    def use(self, board: 'Transcendence.TranscendenceBoard', x: int, y: int) -> Set[tuple]:
        hit_tiles = set()
        for delta in range(0, max(board.height, board.width)):
            tiles = set(
                (x + delta, y + delta),
                (x - delta, y + delta),
                (x + delta, y - delta),
                (x - delta, y - delta),
            )
            for cx, cy in tiles:
                tile = board.get(cx, cy)
                if not Transcendence.Tile.is_breakable(tile):
                    continue

                probability = max(0.1, 1 - (0.15 * delta))
                if random.random() < probability:
                    hit_tiles.add((cx, cy))
        
        return hit_tiles

    def __str__(self):
        return 'Explosion'


class Lightning(Card):
    def __init__(self, level: CardLevel=CardLevel.NORMAL):
        self.level = level

    def use(self, board: 'Transcendence.TranscendenceBoard', x: int, y: int) -> Set[tuple]:
        hit_tiles = set()
        target_count = [2, 4, 6]
        additional_targets = random.randint(-1, target_count[self.level.value])
        if additional_targets < 0:
            hit_tiles.update(
                random.sample(board.destroyed_tiles, k=-additional_targets))
        else:
            hit_tiles.update(
                random.sample(board.breakable_tiles, k=additional_targets))
        return hit_tiles

    def __str__(self):
        return 'Lightning'
