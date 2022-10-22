# %% import packages
import numpy as np
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
            board.place(r, c, copy.deepcopy(piece))
            # if (piece.color == "Black" and r == board.len - 1) \
            #     or (piece.color == "White" and r == 0):
            #     piece.turn_king()
            rc = int((row + r)/2)
            cc = int((col + c)/2)
            captured = copy.copy(board.get(rc, cc))
            board.remove(rc, cc)
            jump_generator(board, r, c, copy.copy(move), moves, results)
            board.place(rc, cc, copy.deepcopy(captured))
            board.remove(r, c)
            board.place(row, col, copy.deepcopy(piece))


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
                board.place(r, c, copy.deepcopy(piece))
                results_all.append(copy.deepcopy(board))
                board.remove(r, c)
                board.place(row, col, copy.deepcopy(piece))
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


def another_color(color):
    if color == 'Black':
        return 'White'
    else:
        return 'Black'


#%% Evaluation functions
def evaluate1(board, color):
    b, B, w, W = 0, 0, 0, 0
    for (x, y) in board.black_position:
        if board.get(x, y).king:
            B += 1
        else:
            b += 1

    for (x, y) in board.white_position:
        if board.get(x, y).king:
            W += 1
        else:
            w += 1

    if color == 'Black':
        if w+W == 0:
            return float('inf')
        return ((b + B * 1.5) - (w + W * 1.5))/(b+B+w+W)
    else:
        if b+B == 0:
            return float('inf')
        return ((w + W * 1.5) - (b + B * 1.5))/(b+B+w+W)


def evaluate2(board, color):
    color_pos = board.get_color_pos(color)
    op_pos = board.get_color_pos(another_color(color))
    if len(op_pos) == 0:
        return float('inf')
    min_dis = 0
    for a in color_pos:
        distances = []
        for b in op_pos:
            distances.append((a[0]-b[0]) ** 2 + (a[1]-b[1]) ** 2)
        min_dis += min(distances)
    return 1 - min_dis/49/2


def evaluate3(board, color):
    length = board.get_len()
    bp, wp = 0, 0
    bk, wk = 0, 0
    bc, wc = 0, 0
    bkd, wkd = 0, 0
    bsd, wsd = 0.0, 0.0
    for row in range(length):
        for col in range(length):
            piece = board.get(row, col)
            if piece:
                r = row if row > (length - (row + 1)) else (length - (row + 1))
                c = col if col > (length - (col + 1)) else (length - (col + 1))
                d = int(((r ** 2.0 + c ** 2.0) ** 0.5) / 2.0)
                if piece.color == 'Black':
                    bc += sum([len(v) for v in \
                               check_jump(board, row, col)])
                    if piece.is_king():
                        bk += 1
                    else:
                        bp += 1
                        bkd += row + 1
                        bsd += d
                else:
                    wc += sum([len(v) for v in \
                               check_jump(board, row, col)])
                    if piece.is_king():
                        wk += 1
                    else:
                        wp += 1
                        wkd += length - (row + 1)
                        wsd += d
    if color == 'Black':
        b_c = 3.125 * (((bp + bk * 2.0) - (wp + wk * 2.0)) + ((bp + bk * 2.0) + (wp + wk * 2.0)))
        black_capture_heuristics = 1.0417 * ((bc - wc) / (1.0 + bc + wc))
        black_kingdist_heuristics = 1.429 * ((bkd - wkd) / (1.0 + bkd + wkd))
        black_safe_heuristics = 5.263 * ((bsd - wsd) / (1.0 + bsd + wsd))
        return b_c + black_capture_heuristics \
               + black_kingdist_heuristics + black_safe_heuristics
    else:
        white_count_heuristics = \
            3.125 * (((wp + wk * 2.0) - (bp + bk * 2.0)) \
                     / 1.0 + ((bp + bk * 2.0) + (wp + wk * 2.0)))
        white_capture_heuristics = 1.0416 * ((wc - bc) / (1.0 + bc + wc))
        white_kingdist_heuristics = 1.428 * ((wkd - bkd) / (1.0 + bkd + wkd))
        white_safe_heuristics = 5.263 * ((wsd - bsd) / (1.0 + bsd + wsd))
        return white_count_heuristics + white_capture_heuristics \
               + white_kingdist_heuristics + white_safe_heuristics


def evaluate(board, color, type=0):
    if type == 0:
        return evaluate1(board, color) + evaluate2(board, color)*0.01
        # return evaluate3(board, color)
    elif type == 1:
        return evaluate1(board, color) + evaluate2(board, color)*0.01
    elif type == 2:
        return evaluate3(board, color)


#%% Alpha-Beta agent
def alpha_beta_search(board, agent_color, maxdepth=float('inf'), heuristic_type=0):
    def max_value(board, color, alpha, beta, depth=1, maxdepth=float('inf')):
        if depth >= maxdepth or is_over(board, color):
            return evaluate(board, agent_color, heuristic_type)
        v = -float('inf')
        moves_all, results_all = all_moves_color(board, color)
        for result in results_all:
            v = max(v, min_value(result, another_color(color), alpha, beta, depth+1, maxdepth))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(board, color, alpha, beta, depth=1, maxdepth=float('inf')):
        if depth >= maxdepth or is_over(board, color):
            return evaluate(board, agent_color, heuristic_type)
        v = float('inf')
        moves_all, results_all = all_moves_color(board, color)
        for result in results_all:
            v = min(v, max_value(result, another_color(color), alpha, beta, depth+1, maxdepth))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    color = agent_color
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
def user_pos_valid(board, piece_position, color):
    if not (piece_position[0].isalpha() and piece_position[1].isnumeric()):
        return False
    else:
        piece_position = position_trans(piece_position)
    if not (0 <= piece_position[0] < board.len) or not (0 <= piece_position[1] < board.len):
        return False
    if board.is_free(piece_position[0], piece_position[1]):
        return False
    if board.get(piece_position[0], piece_position[1]).color != color:
        return False
    return True


def target_pos_valid(board, piece_position, target_position):
    if not (target_position[0].isalpha() and target_position[1].isnumeric()):
        return False
    else:
        target_position = position_trans(target_position)
    all_move = all_moves(board, piece_position[0], piece_position[1])[0]
    next_pos = [move[-1] for move in all_move]
    if target_position not in next_pos:
        return False
    return True


def main_user():
    print("Game start! Let's get ready!")
    user_color = str(input('Please choose the color you want ((Black)/ White):'))
    if user_color not in ["Black", "White"]:
        user_color = "Black"
    agent_color = 'Black' if user_color == 'White' else 'White'

    board = Board()
    board.display()
    color = "Black"
    steps = 1
    while not is_over(board, color) and steps <= 100:
        if user_color == color:
            moves_all, results_all = all_moves_color(board, color)
            piece_valid = [position_trans(move[0]) for move in moves_all]
            target_valid = [position_trans(move[1]) for move in moves_all]
            move2 = [(position_trans(move[0]), position_trans(move[1])) for move in moves_all]

            piece_position = str(input('Please enter the location of the piece you want to move:'))

            while piece_position not in piece_valid:
                piece_position = str(input('The piece is not valid! Please enter again:'))

            target_position = str(input('Please enter the location to move:'))
            while (piece_position, target_position) not in move2:
                target_position = str(input('The move is not valid! Please enter again:'))

            for i, pos in enumerate(target_valid):
                if pos == target_position:
                    board = results_all[i]
                    move = moves_all[i]
            print("The move made is " + " -> ".join(position_trans(pos) for pos in move))
            board.display()
        else:
            print("Please wait...")
            best_action, best_result = alpha_beta_search(board, color, 7)
            board = best_result
            print("The move made is " + " -> ".join(position_trans(pos) for pos in best_action))
            board.display()

        color = another_color(color)
        steps += 1
    print(color + " won!")


def main_depth():
    L = 6
    res = np.zeros((L, L))
    for i in range(1, L+1):
        for j in range(1, L+1):
            board = Board()
            # board.display()
            bb = board
            color = 'Black'
            n = 0
            while n < 200:
                n += 2
                # time.sleep(0.5)
                aa, bb = alpha_beta_search(bb, color, i, 1) #Black
                if aa is None:
                    break
                # print([position_trans(pos) for pos in aa])
                # bb.display()
                # time.sleep(0.5)
                color = another_color(color)
                aa, bb = alpha_beta_search(bb, color, j, 1) #White
                if aa is None:
                    break
                # print([position_trans(pos) for pos in aa])
                # bb.display()
                color = another_color(color)
            if n == 200:
                res[i-1, j-1] = -100
            else:
                if color == 'White':
                    res[i-1, j-1] = 1
                if color == 'Black':
                    res[i-1, j-1] = 2
            print(res)
            # print(another_color(color) + " won!")


def main_depth2():
    import time
    L = 7
    res = np.zeros((L, L))
    board = Board()
    board.display()
    bb = board
    color = 'Black'
    n = 0
    while n < 200:
        n += 2
        time.sleep(2)
        aa, bb = alpha_beta_search(bb, color, 4, 2) #Black
        if aa is None:
            break
        print([position_trans(pos) for pos in aa])
        bb.display()
        time.sleep(2)
        color = another_color(color)
        aa, bb = alpha_beta_search(bb, color, 2, 2) #White
        if aa is None:
            break
        print([position_trans(pos) for pos in aa])
        bb.display()
        color = another_color(color)


def main_evaluation():
    L = 6
    res = np.zeros((1, L))
    for i in range(1, L+1):
        board = Board()
        bb = board
        color = 'Black'
        n = 0
        win = -1
        while n < 200:
            n += 2
            # time.sleep(0.5)
            aa_t, bb_t = alpha_beta_search(bb, color, i, 1)  # Black
            if aa_t is None:
                win = 2
                break
            else:
                aa, bb = aa_t, bb_t
            color = another_color(color)
            aa_t, bb_t = alpha_beta_search(bb, color, i, 2)  # White
            if aa_t is None:
                win = 1
                break
            else:
                aa, bb = aa_t, bb_t
            color = another_color(color)
        if win == -1:
            res[0, i-1] = (len(bb.black_position) - len(bb.white_position))*0.1
        else:
            res[0, i-1] = win
        print(res)


if __name__ == '__main__':
    # board = Board()
    # board.remove(7, 2)
    # board.remove(5, 0)
    # board.place(4, 1, Piece("White"))
    # board.place(3, 2, Piece("Black"))
    # moves = []
    # moves, results = all_moves(board, 3, 2)
    # all_moves_color(board, 'Black')

    import sys
    args = sys.argv[1:]

    if len(args) > 0 and args[0] == '--compare_depth':
        main_depth()
    elif len(args) > 0 and args[0] == '--compare_evaluation':
        main_evaluation()
    else:
        main_user()
