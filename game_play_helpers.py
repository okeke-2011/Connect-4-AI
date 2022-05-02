import copy
import numpy as np


def create_board():
    return [["⚪️" for i in range(7)] for i in range(6)]


def show_board(board):
    template = ["1 ", "2 ", "3 ", "4 ", "5 ", "6 ", "7 "]

    print("\nCurrent Board State:")
    print(template)
    for i in range(len(board)):
        print(board[i])
        print("-------------------------------------------")


def convert_board_to_string(board, player):
    y, r, w = "🟡", "🔴", "⚪️"
    if player == r:
        str_board = "R,"
    elif player == y:
        str_board = "Y,"

    for row in board:
        for cell in row:
            if cell == w:
                str_board += "W"
            elif cell == r:
                str_board += "R"
            elif cell == y:
                str_board += "Y"
    return str_board


# def convert_string_to_board(string):
#     y, r = "🟡", "🔴"
#     board = create_board()
#     pointer = 0
#     string = string.split(",")[1]
#     for i in range(len(board)):
#         for j in range(len(board[i])):
#             if string[pointer] == "W":
#                 pass
#             elif string[pointer] == "R":
#                 board[i][j] = r
#             elif string[pointer] == "Y":
#                 board[i][j] = y
#
#             pointer += 1
#     return board


def get_diagonals(board, bltr=True):
    return_grid = [[] for total in range(12)]
    for i in range(7):
        for j in range(6):
            if bltr:
                return_grid[i + j].append(board[j][i])
            else:
                return_grid[(j - i) % 12].append(board[j][i])
    return return_grid


def retrieve_diagonal(ind):
    lst = []
    if ind < 12:
        for i in range(7):
            for j in range(6):
                if i + j == ind:
                    lst.append([j, i])
    elif ind >= 12:
        ind = ind - 12
        for i in range(7):
            for j in range(6):
                if (j - i) % 12 == ind:
                    lst.append([j, i])
    return lst


def check_win(board):
    y, r, w = "🟡", "🔴", "⚪️"

    diagonals = get_diagonals(board) + get_diagonals(board, False)
    # check diagonals
    for ind, diagonal in enumerate(diagonals):
        if len(diagonal) >= 4:
            for i in range(len(diagonal) - 3):
                if diagonal[i:i + 4] == [r for i in range(4)]:
                    return True, r, retrieve_diagonal(ind)[i:i + 4]
                if diagonal[i:i + 4] == [y for i in range(4)]:
                    return True, y, retrieve_diagonal(ind)[i:i + 4]

    # check rows
    for ind, row in enumerate(board):
        for i in range(4):
            if row[i:i + 4] == [r for i in range(4)]:
                return True, r, [[ind, i + j] for j in range(4)]
            if row[i:i + 4] == [y for i in range(4)]:
                return True, y, [[ind, i + j] for j in range(4)]

    # check columns
    board_t = np.transpose(np.array(board))
    for ind, col in enumerate(board_t):
        for i in range(3):
            if list(col)[i:i + 4] == [r for i in range(4)]:
                return True, r, [[i + j, ind] for j in range(4)]
            if list(col)[i:i + 4] == [y for i in range(4)]:
                return True, y, [[i + j, ind] for j in range(4)]

    return False, None, None


def show_win(board):
    win, player, pos = check_win(board)
    dummy = copy.deepcopy(board)

    if win:
        for row, col in pos:
            dummy[row][col] = "✅ "
    show_board(dummy)


def col_full(board, col):
    w = "⚪️"
    for i in range(6):
        if board[i][col] == w:
            return False
    return True


def full_board(board):
    for col in range(7):
        if not col_full(board, col):
            return False
    return True


def make_move(board, player, col):
    y, r, w = "🟡", "🔴", "⚪️"
    dummy = copy.deepcopy(board)

    if not col_full(dummy, col) and (player == r or player == y):
        for i in range(5, -1, -1):
            if dummy[i][col] == w:
                dummy[i][col] = player
                break
        return dummy
    else:
        return dummy


def possible_moves(board):
    moves = []
    for col in range(7):
        if not col_full(board, col):
            moves.append(col)
    return moves
