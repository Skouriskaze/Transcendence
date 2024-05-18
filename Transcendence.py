from enum import Enum
from typing import Set, Tuple, Dict
from collections import Counter
import Cards



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

    @classmethod
    def is_breakable(tile: 'Tile'):
        if tile in {Tile.NONE, Tile.DESTROYED}:
            return False
        return True


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
        old_tile = self.get(x, y)

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

    def calculate_hit_tiles(self, hit_tiles: Set[Tuple], is_purify: bool = False) -> Counter:
        tile_count = Counter()
        for x, y in hit_tiles:
            tile = self.get(x, y)
            if not Tile.is_breakable(tile):
                raise NotImplementedError(f'Tile of type {tile}'
                                          'is not supported')
            else:
                if tile is Tile.DISTORTED:
                    if is_purify:
                        tile_count[tile] += 1
                        self.set_tile(x, y, Tile.DESTROYED)
                    else:
                        # TODO: Implement hitting distorted tiles. Keep in minnd
                        # that distorted tiles activate after all tiles break.
                        raise NotImplementedError()
                else:
                    tile_count[tile] += 1
                    self.set_tile(x, y, Tile.DESTROYED)

        return tile_count


            # if self.board.get(*hit_tile) is Tile.NORMAL:
            #     self.board.set_tile(*hit_tile, Tile.DESTROYED)
            # elif hit_tile is Tile.DISTORTED:
            #     raise NotImplementedError()
            # else:
            #     raise NotImplementedError(f'Tile of type {hit_tile}'
            #                               'is not supported')

    def __str__(self) -> str:
        output = ''
        for row in self.grid:
            output += ' '.join([str(x.value) for x in row]) + '\n'
        return output


class TranscendenceMove:
    def __init__(self, card: Cards.Card, x: int, y: int):
        self.x = x
        self.y = y
        self.card = card

    def get_hit_tiles(self, board: TranscendenceBoard):
        return self.card.use(board)


class TranscendenceGame:
    def __init__(self, board: TranscendenceBoard):
        self.board = board
        self.hand_left = Cards.Thunder()
        self.hand_right = Cards.Thunder()
        self.queue_first = Cards.Thunder()
        self.queue_second = Cards.Thunder()
        self.queue_third = Cards.Thunder()
        self.turns_left = 0
        self.changes_left = 0

    def bless(self):
        self.changes_left += 1

    def use_left(self, x: int, y: int):
        # TODO: Make sure that the tile used is valid.
        move = TranscendenceMove(self.hand_left, x, y)
        hit_tiles = move.get_hit_tiles(self.board)
        self.board.calculate_hit_tiles(hit_tiles)

        # TODO: Add card moving.

    def __str__(self):
        return str(self.board)