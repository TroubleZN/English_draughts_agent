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
    colors = ['B', 'W']
    kings = ['BK', 'WK']
    isking = False

    def __init__(self, color='B', isking=False):
        if color in self.colors:
            self.color = color
            self.isking = isking
        else:
            raise ValueError("The color should be B or W.")

    def color(self):
        return self.color

    def is_black(self):
        return self.color == 'B'

    def is_white(self):
        return self.color == 'W'

    def is_king(self):
        return self.isking

    def turn_king(self):
        self.isking = True
        if self.color == "B":
            self.color = "BK"
        elif self.color == "W":
            self.color = "WK"

    def turn_pawn(self):
        self.isking = False
        if self.color == "BK":
            self.color = "B"
        elif self.color == "WK":
            self.color = "W"

    def __str__(self):
        return self.color

    def __repr__(self):
        return self.__str__()

