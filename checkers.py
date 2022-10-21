# %% import packages
import numpy as np
import pandas as pd
import copy

# %% Important classes
class Piece(object):
    king = False

    def __init__(self, color='Black', is_king=False):
        if color in ['Black', 'White']:
            self.color = color
            self.king = is_king
        else:
            raise ValueError("The color should be Black or White.")

    def get_color(self):
        return self.color

    def is_king(self):
        return self.king

    def turn_king(self):
        self.king = True

    def turn_soldier(self):
        self.king = False

    def __str__(self):
        king_col = {'Black': 'B', 'White': 'W'}
        soldier_col = {'Black': 'b', 'White': 'w'}
        if self.king:
            return king_col[self.color]
        else:
            return soldier_col[self.color]

    def __repr__(self):
        return self.__str__()


class Board(object):
    def __init__(self):
        self.len = 8
        self.status = [[None for c in range(self.len)] for r in range(self.len)]
        self.black_position = []
        self.white_position = []

        for r in [0, 2]:
            for c in range(1, self.len, 2):
                self.status[r][c] = Piece('Black')
                self.black_position.append((r, c))
        for r in [1]:
            for c in range(0, self.len, 2):
                self.status[r][c] = Piece('Black')
                self.black_position.append((r, c))
        for r in [6]:
            for c in range(1, self.len, 2):
                self.status[r][c] = Piece('White')
                self.white_position.append((r, c))
        for r in [5, 7]:
            for c in range(0, self.len, 2):
                self.status[r][c] = Piece('White')
                self.white_position.append((r, c))

    def is_free(self, row, col):
        return self.status[row][col] is None

    def get_len(self):
        return self.len

    def get(self, row, col):
        return self.status[row][col]

    def remove(self, row, col):
        if self.status[row][col].color == 'Black':
            self.black_position.remove((row, col))
        else:
            self.white_position.remove((row, col))
        self.status[row][col] = None

    def place(self, row, col, piece):
        if piece.color == 'Black':
            self.black_position.append((row, col))
            if row == self.len-1:
                piece.turn_king()
        else:
            self.white_position.append((row, col))
            if row == 0:
                piece.turn_king()
        self.status[row][col] = piece

    def get_color_pos(self, color = 'Black'):
        if color == 'Black':
            return self.black_position
        elif color == 'White':
            return self.white_position

    def is_empty(self):
        for r in range(self.len):
            for c in range(self.len):
                if not self.is_free(r, c):
                    return False
        return True

    def is_full(self):
        for r in range(self.len):
            for c in range(self.len):
                if self.is_free(r, c):
                    return False
        return True

    def display(self):
        print(self)

    def __str__(self):
        vline = '\n' + (' ' * 2) + ('+---' * self.len) + '+' + '\n'
        numline = ' '.join([(' ' + str(i) + ' ') for i in range(1, self.len + 1)])
        str_ = (' ' * 3) + numline + vline
        for r in range(0, self.len):
            str_ += chr(97 + r) + ' |'
            for c in range(0, self.len):
                str_ += ' ' + \
                        (str(self.status[r][c]) if self.status[r][c] is not None else ' ') + ' |'
            str_ += vline
        return str_

    def __repr__(self):
        return self.__str__()


# %% Move and jump check
def check_simple_move(board, row, col):
    length = board.get_len()
    piece = board.get(row, col)
    simple_move = []
    if piece:
        color = piece.get_color()
        king = piece.is_king()
        if color == 'Black':
            down = [(-1, -1), (-1, +1)]
            up = [(+1, -1), (+1, +1)]
        else:
            up = [(-1, -1), (-1, +1)]
            down = [(+1, -1), (+1, +1)]
        for (x, y) in up:
            if (0 <= row + x < length) and (0 <= col + y < length) and board.is_free(row + x, col + y):
                simple_move.append((x, y))
        if king:
            for (x, y) in down:
                if (0 <= row + x < length) and (0 <= col + y < length) and board.is_free(row + x, col + y):
                    simple_move.append((x, y))
    return simple_move


def check_jump(board, row, col):
    length = board.get_len()
    piece = board.get(row, col)
    jumps = []
    if piece:
        color = piece.get_color()
        king = piece.is_king()
        if color == 'Black':
            down = [(-1, -1), (-1, +1)]
            up = [(+1, -1), (+1, +1)]
        else:
            up = [(-1, -1), (-1, +1)]
            down = [(+1, -1), (+1, +1)]
        for (x, y) in up:
            if (0 <= row + 2 * x < length) \
                    and (0 <= col + 2 * y < length) \
                    and not board.is_free(row + x, col + y) \
                    and board.get(row + x, col + y).get_color() != piece.get_color() \
                    and board.is_free(row + 2 * x, col + 2 * y):
                jumps.append((2 * x, 2 * y))
        for (x, y) in down:
            if king \
                    and (0 <= row + 2 * x < length) \
                    and (0 <= col + 2 * y < length) \
                    and not board.is_free(row + x, col + y) \
                    and board.get(row + x, col + y).get_color() != piece.get_color() \
                    and board.is_free(row + 2 * x, col + 2 * y):
                jumps.append((2 * x, 2 * y))
    return jumps


def jump_generator(board, row, col, move, moves, results):
    move.append((row, col))
    jumps = check_jump(board, row, col)
    if not jumps:
        moves.append(move)
        results.append(copy.deepcopy(board))
    else:
        for jump in jumps:
            (r, c) = (row + jump[0], col + jump[1])
            piece = copy.copy(board.get(row, col))
            board.remove(row, col)
            board.place(r, c, piece)
            if (piece.color == "Black" and r == board.len - 1) \
                or (piece.color == "White" and r == 0):
                piece.turn_king()
            rc = int((row + r)/2)
            cc = int((col + c)/2)
            captured = copy.copy(board.get(rc, cc))
            board.remove(rc, cc)
            jump_generator(board, r, c, copy.copy(move), moves, results)
            board.place(rc, cc, captured)
            board.remove(r, c)
            board.place(row, col, piece)


def all_moves(board, row, col):
    moves = []
    results = []
    jump_generator(board, row, col, [], moves, results)
    if moves == [[(row, col)]]:
        moves = []
        results = []
    if not moves:
        simple_moves = check_simple_move(board, row, col)
        for simple_move in simple_moves:
            moves.append([(row, col), (row + simple_move[0], col + simple_move[1])])
    return moves, results


def all_moves_color(board, color):
    jumped = False
    moves_all = []
    results_all = []
    for (row, col) in board.get_color_pos(color):
        moves = []
        results = []
        jump_generator(board, row, col, [], moves, results)
        if moves != [[(row, col)]]:
            jumped = True
            moves_all += moves
            results_all += results

    if not jumped:
        pos_list = copy.deepcopy(board.get_color_pos(color))
        for (row, col) in pos_list:
            simple_moves = check_simple_move(board, row, col)
            for simple_move in simple_moves:
                r = row + simple_move[0]
                c = col + simple_move[1]
                moves_all.append([(row, col), (r, c)])
                piece = copy.copy(board.get(row, col))
                board.remove(row, col)
                board.place(r, c, piece)
                results_all.append(copy.deepcopy(board))
                board.remove(r, c)
                board.place(row, col, piece)
    return moves_all, results_all


# %% Game essential functions
def is_over(board, color='Black'):
    length = board.get_len()
    for (r, c) in board.get_color_pos(color):
        moves = all_moves(board, r, c)
        if moves:
            return False
    return True


def position_trans(old_pos):
    if str(old_pos).isalnum():
        return ord(old_pos[0]) - 97, int(old_pos[1]) - 1
    else:
        return chr(old_pos[0] + 97) + str(old_pos[1] + 1)


def evaluate1(board, color):
    b, B, w, W = 0, 0, 0, 0
    for (x, y) in board.black_position:
        if board.get(x,y).king:
            B += 1
        else:
            b += 1

    for (x, y) in board.white_position:
        if board.get(x, y).king:
            W += 1
        else:
            w += 1

    if color == 'Black':
        return (b + B * 2) - (w + W * 1)
    else:
        return (w + W * 2) - (b + B * 1)


def evaluate2(board, color):
    print(1)


def evaluate(board, color):
    return evaluate1(board, color)


def another_color(color):
    if color == 'Black':
        return 'White'
    else:
        return 'Black'


#%% Agents
def alpha_beta_search(board, agent_color, maxdepth=float('inf')):
    color = agent_color
    def max_value(board, color, alpha, beta, depth=1, maxdepth=float('inf')):
        if depth >= maxdepth or is_over(board, color):
            return evaluate1(board, color)
        v = -float('inf')
        depth += 1
        moves_all, results_all = all_moves_color(board, color)
        for result in results_all:
            v = max(v, min_value(result, another_color(color), alpha, beta, depth, maxdepth))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(board, color, alpha, beta, depth=1, maxdepth=float('inf')):
        if depth >= maxdepth or is_over(board, color):
            return evaluate(board, color)
        depth += 1
        v = float('inf')
        moves_all, results_all = all_moves_color(board, color)
        for result in results_all:
            v = min(v, max_value(result, another_color(color), alpha, beta, depth, maxdepth))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alpha_beta_search:
    best_score = -float('inf')
    beta = float('inf')
    best_action = None
    best_result = None
    moves_all, results_all = all_moves_color(board, color)
    for i, result in enumerate(results_all):
        v = min_value(result, another_color(color), best_score, beta, 1, maxdepth)
        if v > best_score:
            best_score = v
            best_action = moves_all[i]
            best_result = copy.deepcopy(result)
    return best_action, best_result



# %% Main part
def main_user():
    print("Game start! Let's get ready!")
    user_color = str(input('Please choose the color you want ((Black)/ White):'))
    if user_color not in ["Black", "White"]:
        user_color = "Black"
    agent_color = 'Black' if user_color == 'White' else 'White'

    board = Board()
    color = "Black"
    steps = 1
    moves = [1]
    while moves and steps <= 10:
        if user_color == color:
            board.display()
            piece_position = str(input('Please enter the location of the piece you want to move:'))

            while not (piece_position[0].isalpha() and piece_position[1].isnumeric()):
                piece_position = str(input('The piece is not valid! Please enter again:'))
            piece_position = position_trans(piece_position)

            moves = all_moves(board, piece_position[0], piece_position[1])
            next_pos = [move[1] for move in moves]

            while not moves or not board.get(piece_position[0], piece_position[1]) or user_color != board.get(piece_position[0], piece_position[1]).color:
                piece_position = str(input('1The piece is not valid! Please enter again:'))
                if piece_position.isalnum():
                    piece_position = position_trans(piece_position)

            target_position = str(input('Please enter the location to move:'))
            while not (target_position[0].isalpha() and target_position[1].isnumeric()):
                target_position = str(input('The move is not valid! Please enter again:'))
            if target_position.isalnum():
                target_position = position_trans(target_position)
            while target_position not in next_pos:
                target_position = str(input('The move is not valid! Please enter again:'))
                if target_position.isalnum():
                    target_position = position_trans(target_position)


        color = 'Black' if color == 'White' else 'White'
        steps += 1
    print(color + " won!")


if __name__ == '__main__':
    board = Board()
    # board.remove(7, 2)
    # board.remove(5, 0)
    # board.place(4, 1, Piece("White"))
    # board.place(3, 2, Piece("Black"))
    # moves = []
    # moves, results = all_moves(board, 3, 2)
    # all_moves_color(board, 'Black')

    import time

    board.display()
    bb = board
    while 1:
        # time.sleep(0.5)
        aa, bb = alpha_beta_search(bb, 'Black', 3)
        if aa is None:
            break
        print([position_trans(pos) for pos in aa])
        bb.display()
        # time.sleep(0.5)
        aa, bb = alpha_beta_search(bb, 'White', 5)
        if aa is None:
            break
        print([position_trans(pos) for pos in aa])
        bb.display()
    print('Game over!')
    # main_user()
