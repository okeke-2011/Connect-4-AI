import numpy as np
from game_play_helpers import *


def convert_ai_move_to_string(search_result):
    if search_result is None:
        return "None"
    else:
        return str(search_result[0]) + "," + str(search_result[1])


def convert_str_to_ai_move(string):
    if string == "None":
        return None
    else:
        value, move = string.split(",")
        return float(value), int(move)


def is_terminal(board):
    return full_board(board) or check_win(board)[0]


def utility(board, player):
    y, r = "🟡", "🔴"
    if player != r and player != y:
        return None
    if full_board(board) and not check_win(board)[0]:
        return 0
    elif check_win(board)[0] and check_win(board)[1] == player:
        return 1000
    elif check_win(board)[0] and check_win(board)[1] != player:
        return -1000
    else:
        return None


def eval_func(board, player):
    y, r, w = "🟡", "🔴", "⚪️"
    Y, R = [0 for i in range(3)], [0 for i in range(3)]

    if is_terminal(board):
        return utility(board, player)

    diags = [d for d in get_diagonals(board) + get_diagonals(board, False) if len(d) >= 4]
    board_t = np.transpose(np.array(board))
    all_4 = []

    for row in board:
        for i in range(len(row) - 3):
            all_4.append(row[i:i + 4])

    for col in board_t:
        for i in range(len(col) - 3):
            all_4.append(list(col)[i:i + 4])

    for diag in diags:
        for i in range(len(diag) - 3):
            all_4.append(diag[i:i + 4])

    for item in all_4:
        if item.count(r) == 3 and item.count(w) == 1:
            R[2] = R[2] + 1
        if item.count(y) == 3 and item.count(w) == 1:
            Y[2] = Y[2] + 1
        if item.count(r) == 2 and item.count(w) == 2:
            R[1] = R[1] + 1
        if item.count(y) == 2 and item.count(w) == 2:
            Y[1] = Y[1] + 1
        if item.count(r) == 1 and item.count(w) == 3:
            R[0] = R[0] + 1
        if item.count(y) == 1 and item.count(w) == 3:
            Y[0] = Y[0] + 1

    if player == r:
        return 9 * R[2] + 3 * R[1] + R[0] - (9 * Y[2] + 3 * Y[1] + Y[0])
    else:
        return 9 * Y[2] + 3 * Y[1] + Y[0] - (9 * R[2] + 3 * R[1] + R[0])