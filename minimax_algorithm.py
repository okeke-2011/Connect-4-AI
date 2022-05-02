import numpy as np
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import declarative_base, sessionmaker

from ai_helpers import *
from game_play_helpers import *


engine = create_engine("sqlite:///connect_4_db.sqlite3")
Base = declarative_base()


class SavedMoves(Base):
    __tablename__ = "saved_moves"
    board_state = Column(String, primary_key=True)
    optimal_move = Column(String, primary_key=True)


def memoize_search(search):
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    def inner(board, player):
        new_state = False
        target_board_state = convert_board_to_string(board, player)
        found_board = session.query(SavedMoves).filter_by(board_state=target_board_state).first()

        if found_board is None:
            new_state = True
            str_optimal_move = convert_ai_move_to_string(search(board, player))
            new_saved_move = SavedMoves(board_state=target_board_state,
                                        optimal_move=str_optimal_move)
            session.add(new_saved_move)
            session.commit()
        else:
            str_optimal_move = found_board.optimal_move

        return convert_str_to_ai_move(str_optimal_move), new_state

    return inner


@memoize_search
def alpha_beta_search(board, current_player):
    max_depth = 5
    value, move = max_value(board, -np.inf, np.inf, current_player, 0, max_depth)
    if move is not None:
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
