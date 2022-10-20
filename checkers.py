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
        else:
            self.white_position.append((row, col))
        self.status[row][col] = piece

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
def check_move(board, row, col):
    length = board.get_len()
    piece = board.get(row, col)
    moves = []
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
                moves.append((x, y))
        if king:
            for (x, y) in down:
                if (0 <= row + x < length) and (0 <= col + y < length) and board.is_free(row + x, col + y):
                    moves.append((x, y))
    return moves


def check_jump(board, row, col):
    length = board.get_len()
    piece = board.get(row, col)
    jumps = []
    if piece:
        color = piece.get_color()
        king = piece.is_king()
        if color == 'Black':
            up = [(-1, -1), (-1, +1)]
            down = [(+1, -1), (+1, +1)]
        else:
            down = [(-1, -1), (-1, +1)]
            up = [(+1, -1), (+1, +1)]
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


# %% Game essential functions
def is_over(board, color='Black'):
    length = board.get_len()
    if color == 'White':
        for (r, c) in board.white_position:
            moves = check_move(board, r, c)
            jumps = check_jump(board, r, c)
            if moves or jumps:
                return False
    if color == 'Black':
        for (r, c) in board.black_position:
            moves = check_move(board, r, c)
            jumps = check_jump(board, r, c)
            if moves or jumps:
                return False
    return True


def position_trans(old_pos):
    if str(old_pos).isalnum():
        return ord(old_pos[0]) - 97, int(old_pos[1]) - 1
    else:
        return chr(old_pos[0] + 97) + str(old_pos[1] + 1)


def evaluate(board):

# %% Main part
def main():
    user_color = str(input('Please choose the color you want (Black/ White):'))
    agent_color = 'Black' if user_color == 'White' else 'White'

    board = Board()

    piece_position = str(input('Please enter the location of the piece you want to move:'))
    if piece_position.isalnum():
        piece_position = position_trans(piece_position)
    target_position = str(input('Please enter the location to move:'))
    if target_position.isalnum():
        target_position = position_trans(target_position)


if __name__ == '__main__':
    main()
