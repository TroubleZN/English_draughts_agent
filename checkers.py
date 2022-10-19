#%% import packages
import numpy as np
import pandas as pd


#%% Important classes
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
        for r in [0, 2]:
            for c in range(1, self.len, 2):
                self.status[r][c] = Piece('Black')
        for r in [1]:
            for c in range(0, self.len, 2):
                self.status[r][c] = Piece('Black')
        for r in [-2]:
            for c in range(1, self.len, 2):
                self.status[r][c] = Piece('White')
        for r in [-1, -3]:
            for c in range(0, self.len, 2):
                self.status[r][c] = Piece('White')

    def is_free(self, row, col):
        return self.status[row][col] is None

    def place(self, row, col, piece):
        self.status[row][col] = piece

    def get_len(self):
        return self.len

    def get(self, row, col):
        return self.status[row][col]

    def remove(self, row, col):
        self.status[row][col] = None

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


#%% Vital function related to the game rule
def is_over(state):
    board = state[0]
    turn = state[1]
    depth = state[2]
    (moves, captures) = crank.get_hints(board, turn)
    if maxdepth is not None:
        return ((not moves) and (not captures)) or depth >= maxdepth
    else:
        return ((not moves) and (not captures))


def alpha_beta_agent(state):

def move_generator(board, row, col):
    length = board.get_len()
    piece = board.get(row, col)
    moves = []
    if piece:
        color = piece.get_color()
        king = piece.is_king()
        if color == 'Black':
            up = [(-1, -1), (-1, +1)]
            down = [(+1, -1), (+1, +1)]
        else:
            down = [(-1, -1), (-1, +1)]
            up = [(+1, -1), (+1, +1)]
        if king:
            for move in up:
                if board.is_free(row + move[0], col + move[1]):
                    moves.append(move)
            for move in down:
                if board.is_free(row + move[0], col + move[1]):
                    moves.append(move)
        else:
            for move in up:
                if board.is_free(row + move[0], col + move[1]):
                    moves.append(move)
    return moves

def jump_generator(board, row, col):
    length = board.get_len()
    piece = board.get(row, col)
    jumps = []
    if piece:
        color = piece.get_color()
        king = piece.is_king()




def evaluate(state):




