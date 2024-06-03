import Transcendence
import itertools
import json
import Cards
from typing import List

class GameWrapper:
    def __init__(self, game: 'Transcendence.TranscendenceGame'):
        self.game = game

    def make_move(self, move: 'Transcendence.TranscendenceMove'):
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
        Cards.Thunder: 0,
        Cards.Tornado: 1,
        Cards.Purify: 2,
        Cards.Tempest: 3,
        Cards.Hellfire: 4,
        Cards.Shockwave: 5,
        Cards.Earthquake: 6,
        Cards.TidalWave: 7,
        Cards.Explosion: 8,
        Cards.Lightning: 9,
        Cards.Tree: 10,
        Cards.Outburst: 11,
    }

    INT_TO_CARD = {v: k for k, v in CARD_TO_INT.items()}

class ToJson:
    @classmethod
    def board_to_dict(cls, board: 'Transcendence.TranscendenceBoard'):
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
        board = Transcendence.TranscendenceBoard(width, height)
        raw_grid = board_dict.get('grid')
        for x in range(width):
            for y in range(height):
                board.set_tile(x, y, Transcendence.Tile(raw_grid[y][x]))
        return board

    @classmethod
    def card_to_serializable(cls, card: 'Cards.Card'):
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
    def move_to_json(cls, move: 'Transcendence.TranscendenceMove'):
        output = {}
        output['x'] = move.x
        output['y'] = move.y
        output['card'] = ToJson.card_to_serializable(move.card)
        output['is_left'] = move.is_left
        output['is_change'] = move.is_change
        return json.dumps(output)

    @classmethod
    def json_to_move(cls, move_json: dict) -> 'Transcendence.TranscendenceMove':
        move_dict = json.loads(move_json)
        move_dict['card'] = ToJson.serializable_to_card(move_dict['card'])
        move = Transcendence.TranscendenceMove(
            **move_dict
        )
        return move
        
    @classmethod
    def game_to_json(cls, game: 'Transcendence.TranscendenceGame'):
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
        game = Transcendence.TranscendenceGame(board)
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