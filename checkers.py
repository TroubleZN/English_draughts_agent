#%% import packages
import numpy as np
import pandas as pd


#%% Important classes
class Board(object):
    def __init__(self):
        self.len = 8
        self.status = [[None for c in range(self.len)] for r in range(self.len)]

    def get_cells(self):
        return self.status

    def is_free(self, row, col):
        return self.status[row][col] is None

    def place(self, row, col, piece):
        self.status[row][col] = piece

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

class Move(object):
    