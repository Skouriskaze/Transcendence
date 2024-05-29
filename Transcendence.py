from enum import Enum
from typing import Set, Tuple, Dict
from collections import Counter
import Cards
import Generators
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

    @classmethod
    def is_breakable(cls, tile: 'Tile'):
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
        self.destroyed_tiles = set()
        self.unusable_tiles = set()
        self._populate_tiles()

    def _add_tile_metadata(self, x, y, tile):
        if tile is Tile.NONE:
            self.unusable_tiles.add((x, y))
        elif tile is Tile.DISTORTED:
            self.distorted_tiles.add((x, y))
        elif tile is Tile.DESTROYED:
            self.destroyed_tiles.add((x, y))
        else:
            self.breakable_tiles.add((x, y))

    def _remove_tile_metadata(self, x, y, tile):
        if tile is Tile.NONE:
            self.unusable_tiles.remove((x, y))
        elif tile is Tile.DISTORTED:
            self.distorted_tiles.remove((x, y))
        elif tile is Tile.DESTROYED:
            self.destroyed_tiles.remove((x, y))
        else:
            self.breakable_tiles.remove((x, y))

    def _populate_tiles(self) -> None:
        self.breakable_tiles.clear()
        self.distorted_tiles.clear()
        self.unusable_tiles.clear()
        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                self._add_tile_metadata(x, y, tile)

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

        self._add_tile_metadata(x, y, tile)
        self._remove_tile_metadata(x, y, old_tile)

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
                # TODO: Implement breakable tiles being undone.
                # In the case of lightning.
                raise NotImplementedError(f'Tile of type {tile}'
                                          'is not supported')
            else:
                if tile is Tile.DISTORTED:
                    if is_purify:
                        tile_count[tile] += 1
                        self.set_tile(x, y, Tile.DESTROYED)
                    else:
                        # TODO: Implement hitting distorted tiles. Keep in mind
                        # that distorted tiles activate after all tiles break.
                        raise NotImplementedError()
                else:
                    tile_count[tile] += 1
                    self.set_tile(x, y, Tile.DESTROYED)

        return tile_count

    def __str__(self) -> str:
        output = ''
        for row in self.grid:
            output += ' '.join([str(x.value) for x in row]) + '\n'
        return output


class TranscendenceMove:
    def __init__(self, card: Cards.Card, x: int, y: int, is_left: bool = True):
        self.x = x
        self.y = y
        self.card = card
        self.is_left = is_left

    def get_hit_tiles(self, board: TranscendenceBoard, x: int, y: int):
        return self.card.use(board, x, y)


class TranscendenceGame:
    def __init__(self, board: TranscendenceBoard):
        self.board = board
        self.hand_left = Cards.Thunder()
        self.hand_right = Cards.Tornado()
        self.hand_queue = [Cards.Lightning(), Cards.Tempest(), Cards.Purify()]
        self.hand_queue_size = 3
        self.turns_left = 0
        self.changes_left = 0

    def bless(self, move: TranscendenceMove) -> None:
        self.turns_left += 1

    def add(self, move: TranscendenceMove) -> None:
        self.changes_left += 1

    def enhance(self, move: TranscendenceMove) -> None:
        if move.is_left:
            self.hand_right.enhance()
        else:
            self.hand_left.enhance()

    def clone(self, move: TranscendenceMove) -> None:
        if move.is_left:
            self.hand_right = move.card
        else:
            self.hand_left = move.card

    def mystery(self, move: TranscendenceMove) -> None:
        result = None
        if random.choice([True, False]):
            result = Cards.Tree()
        else:
            result = Cards.Outburst()

        if move.is_left:
            self.hand_right = result
        else:
            self.hand_left = result


    def relocation(self, move: TranscendenceMove) -> None:
        raise NotImplementedError()

    def use_left(self, x: int, y: int):
        move = TranscendenceMove(self.hand_left, x, y, is_left=True)
        self.use_move(move)

    def use_move(self, move: TranscendenceMove):
        # Ensure the move is on a valid tile.
        if (move.x, move.y) not in self.board.breakable_tiles:
            if ((move.x, move.y) in self.board.distorted_tiles
                and isinstance(move.card, Cards.Purify)):
                pass
        hit_tiles = move.get_hit_tiles(self.board, move.x, move.y)
        tile_counter = self.board.calculate_hit_tiles(hit_tiles)

        if Tile.BLESSING in tile_counter:
            self.bless(move)
        if Tile.ADDITION in tile_counter:
            self.add(move)
        if Tile.CLONE in tile_counter:
            self.clone(move)
        if Tile.ENHANCEMENT in tile_counter:
            self.enhance(move)
        if Tile.MYSTERY in tile_counter:
            self.mystery(move)
        if Tile.RELOCATION in tile_counter:
            self.relocation(move)

        # TODO: Add all fancy tiles.
        # TODO: Add card moving. Include card generation.
        # TODO: Add new board generation. Namely enhanced tile.
        # TODO: Add 

        self.fix_hand()

    def fix_hand(self) -> None:
        # How to fix hand:
        # 1. Fill in left and right hand slots.
        # 2. Merge hands if needed. Fold right into left.
        # 3. Fill in hand slots.
        # 4. Merge hands if needed...
        # 5. Continue until both hand slots are full.
        self._fold_hand()
        self._refill_hand_queue()
        while self.hand_left is None or self.hand_right is None:
            if self.hand_left is None:
                self.hand_left = self.hand_queue.pop(0)
            if self.hand_right is None:
                self.hand_right = self.hand_queue.pop(0)
            self._fold_hand()
            self._refill_hand_queue()

    def _fold_hand(self) -> None:
        if self.hand_left is None or self.hand_right is None:
            return
        if type(self.hand_left) is type(self.hand_right):
            if not (self.hand_left.level is Cards.CardLevel.MAX
                or self.hand_right.level is Cards.CardLevel.MAX):
                self.hand_right = None
                self.hand_left.enhance()

    def _refill_hand_queue(self) -> None:
        while len(self.hand_queue) < self.hand_queue_size:
            self.hand_queue.append(Generators.CardGenerator.get_random_card())

    def __str__(self):
        return str(self.board)