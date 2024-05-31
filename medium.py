import Transcendence
import itertools

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
            for (left, right) in itertools.zip_longest(output, right_list, fillvalue=''):
                new_output.append(left + str.ljust(right, right_len))
            output = new_output

        return '\n'.join(output)