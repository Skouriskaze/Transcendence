import json
import itertools

from . import cards
from . import transcendence


from typing import List

class GameWrapper:
    def __init__(self, game: 'transcendence.TranscendenceGame'):
        self.game = game

    def make_move(self, move: 'transcendence.TranscendenceMove'):
        output = []
        board1 = str(self.game).split('\n')
        move_list = str(move).split('\n')

        self.game.use_move(move)

        board2 = str(self.game).split('\n')

        to_add = [board1, move_list, board2]
        for right_list in to_add:
            right_len = max([len(x) + 1 for x in right_list])
            new_output = []
            for (left, right) in itertools.zip_longest(
                output, right_list, fillvalue=''):
                new_output.append(left + str.ljust(right, right_len))
            output = new_output

        return '\n'.join(output)


class _CardConstants:
    CARD_TO_INT = {
        cards.Thunder: 0,
        cards.Tornado: 1,
        cards.Purify: 2,
        cards.Tempest: 3,
        cards.Hellfire: 4,
        cards.Shockwave: 5,
        cards.Earthquake: 6,
        cards.TidalWave: 7,
        cards.Explosion: 8,
        cards.Lightning: 9,
        cards.Tree: 10,
        cards.Outburst: 11,
    }

    INT_TO_CARD = {v: k for k, v in CARD_TO_INT.items()}

class ToJson:
    @classmethod
    def board_to_dict(cls, board: 'transcendence.TranscendenceBoard'):
        output = {}
        grid = [[tile.value for tile in row] for row in board.grid]
        output['grid'] = grid
        output['width'] = board.width
        output['height'] = board.height
        return output

    @classmethod
    def dict_to_board(cls, board_dict: dict):
        width = board_dict.get('width')
        height = board_dict.get('height')
        board = transcendence.TranscendenceBoard(width, height)
        raw_grid = board_dict.get('grid')
        for x in range(width):
            for y in range(height):
                board.set_tile(x, y, transcendence.Tile(raw_grid[y][x]))
        return board

    @classmethod
    def card_to_serializable(cls, card: 'cards.Card'):
        card_int = _CardConstants.CARD_TO_INT[type(card)]
        card_level = card.level.value
        return (card_int, card_level)

    @classmethod
    def serializable_to_card(cls, card: List):
        if not card:
            raise ValueError()
        card_class = _CardConstants.INT_TO_CARD[card[0]]
        card_level = card[1]
        return card_class(card_level)

    @classmethod
    def move_to_json(cls, move: 'transcendence.TranscendenceMove'):
        output = {}
        output['x'] = move.x
        output['y'] = move.y
        output['card'] = ToJson.card_to_serializable(move.card)
        output['is_left'] = move.is_left
        output['is_change'] = move.is_change
        return json.dumps(output)

    @classmethod
    def json_to_move(cls, move_json: dict) -> 'transcendence.TranscendenceMove':
        move_dict = json.loads(move_json)
        move_dict['card'] = ToJson.serializable_to_card(move_dict['card'])
        move = transcendence.TranscendenceMove(
            **move_dict
        )
        return move
        
    @classmethod
    def game_to_json(cls, game: 'transcendence.TranscendenceGame'):
        output = {}
        output['board'] = ToJson.board_to_dict(game.board)
        output['hand_left'] = ToJson.card_to_serializable(game.hand_left)
        output['hand_right'] = ToJson.card_to_serializable(game.hand_right)
        output['hand_queue'] = [ToJson.card_to_serializable(card)
                                for card in game.hand_queue]
        output['turns_left'] = game.turns_left
        output['changes_left'] = game.changes_left
        return json.dumps(output)

    @classmethod
    def json_to_game(cls, game_json: dict):
        game_dict = json.loads(game_json)
        board_dict = game_dict.get('board')
        board = ToJson.dict_to_board(board_dict)
        game = transcendence.TranscendenceGame(board)
        game.hand_left = ToJson.serializable_to_card(game_dict.get('hand_left'))
        game.hand_right = ToJson.serializable_to_card(
            game_dict.get('hand_right'))
        if game_dict.get('hand_queue'):
            game.hand_queue = [ToJson.serializable_to_card(card_value)
                                    for card_value
                                    in game_dict.get('hand_queue')]
        game.turns_left = game_dict.get('turns_left')
        game.changes_left = game_dict.get('changes_left')
        return game