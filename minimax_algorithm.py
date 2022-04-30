import numpy as np
from sqlalchemy import create_engine, String
from sqlalchemy.orm import declarative_base

from ai_helpers import *
from game_play_helpers import *


engine = create_engine("sqlite:///connect_4_db.sqlite3")
Base = declarative_base()


def memoize_search(search):
    memory = {}

    def inner(board, player):
        if str(board) + player not in memory:
            memory[str(board) + player] = search(board, player)
        return memory[str(board) + player]

    return inner


@memoize_search
def alpha_beta_search(board, current_player):
    max_depth = 5
    value, move = max_value(board, -np.inf, np.inf, current_player, 0, max_depth)
    if move != None:
        return value, move
    else:
        return None


def max_value(board, alpha, beta, current_player, depth, max_depth):
    if is_terminal(board):
        return utility(board, current_player), None
    v = -np.inf
    for a in possible_moves(board):
        sim_player = current_player
        new_board = make_move(board, sim_player, a)

        if depth >= max_depth:
            v2, a2 = eval_func(new_board, current_player), a
        else:
            v2, a2 = min_value(new_board, alpha, beta, current_player, depth + 1, max_depth)

        if v2 > v:
            v, move = v2, a
            alpha = max(alpha, v)

        if v >= beta:
            return v, move
    return v, move


def min_value(board, alpha, beta, current_player, depth, max_depth):
    y, r = "🟡", "🔴"
    if is_terminal(board):
        return utility(board, current_player), None
    v = np.inf
    for a in possible_moves(board):
        if current_player == r:
            sim_player = y
        else:
            sim_player = r
        new_board = make_move(board, sim_player, a)

        if depth >= max_depth:
            v2, a2 = eval_func(new_board, current_player), a
        else:
            v2, a2 = max_value(new_board, alpha, beta, current_player, depth + 1, max_depth)

        if v2 < v:
            v, move = v2, a
            beta = min(beta, v)

        if v <= alpha:
            return v, move
    return v, move
