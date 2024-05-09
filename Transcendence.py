from enum import Enum
from typing import List

import random

class Tile(Enum):
    NONE = 0
    NORMAL = 1
    DESTROYED = 2
    DISTORTED = 3
    ADDITION = 4
    RELOCATION = 5
    CLONE = 6
    BLESSING = 7
    MYSTERY = 8
    ENHANCEMENT = 9


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
    

class TranscendenceBoard:
    # TODO: Add a function for relocation.
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[Tile.NORMAL for _ in range(width)] for _ in range(height)]
        self.breakable_tiles = set()
        self.distorted_tiles = set()
        self.unusable_tiles = set()
        self._populate_tiles()

    def _populate_tiles(self) -> None:
        self.breakable_tiles.clear()
        self.distorted_tiles.clear()
        self.unusable_tiles.clear()
        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                if tile is Tile.NONE:
                    self.unusable_tiles.add((x, y))
                elif tile is Tile.DISTORTED:
                    self.distorted_tiles.add((x, y))
                else:
                    self.breakable_tiles.add((x, y))

    def set_tile(self, x: int, y: int, tile: Tile) -> None:
        if not self.in_board(x, y):
            return None

        old_tile = self.grid[y][x]
        if old_tile is Tile.NONE:
            return None

        self.setup_board_tile(x, y, tile)

    def setup_board_tile(self, x: int, y: int, tile: Tile) -> None:
        if not self.in_board(x, y):
            return None
        old_tile = self.grid[y][x]

        self.grid[y][x] = tile

        if tile is Tile.NONE:
            self.unusable_tiles.add((x, y))
        elif tile is Tile.DISTORTED:
            self.distorted_tiles.add((x, y))
        else:
            self.breakable_tiles.add((x, y))

        if old_tile is Tile.NONE:
            self.unusable_tiles.remove((x, y))
        elif old_tile is Tile.DISTORTED:
            self.distorted_tiles.remove((x, y))
        else:
            self.breakable_tiles.remove((x, y))

    def in_board(self, x: int, y: int) -> bool:
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    def get(self, x: int, y: int) -> Tile:
        if not self.in_board(x, y):
            return None
        return self.grid[y][x]

    def isFinished(self):
        return len(self.breakable_tiles) == 0

    def __str__(self) -> str:
        output = ''
        for row in self.grid:
            output += ' '.join([str(x.value) for x in row]) + '\n'
        return output

class TranscendenceGame:
    def __init__(self, board: TranscendenceBoard):
        self.board = board
        self.hand_left = Thunder()
        self.hand_right = Thunder()
        self.queue_first = Thunder()
        self.queue_second = Thunder()
        self.queue_third = Thunder()
        self.turns_left = 0
        self.changes_left = 0

    def bless(self):
        self.changes_left += 1

    def use_left(self, x: int, y: int):
        # TODO: Make sure that the tile used is valid.
        hit_tiles = self.hand_left.use(self.board, x, y)
        for hit_tile in hit_tiles:
            if self.board.get(*hit_tile) is Tile.NORMAL:
                self.board.set_tile(*hit_tile, Tile.DESTROYED)
            elif hit_tile is Tile.DISTORTED:
                raise NotImplementedError()
            else:
                raise NotImplementedError(f'Tile of type {hit_tile}'
                                          'is not supported')

        # TODO: Add card moving.

    def __str__(self):
        return str(self.board)