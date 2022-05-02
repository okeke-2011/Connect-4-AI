import time
import random

from minimax_algorithm import *


def generate_move(board, move_generation="normal"):
    if move_generation == "uniform":
        weights = {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}
    elif move_generation == "side_biased":
        weights = {0: 4, 1: 3, 2: 2, 3: 1, 4: 2, 5: 3, 6: 4}
    else:
        weights = {0: 1, 1: 2, 2: 3, 3: 4, 4: 3, 5: 2, 6: 1}

    moves = possible_moves(board)
    chance_list = []
    for move in moves:
        chance_list += [move] * weights[move]

    return random.choice(chance_list)


def run_training_session():
    num_sessions = int(input("How many sessions do you want to run?"))
    start_first = int(input("How many sessions should the ai start first?"))
    num_rounds = int(input("Set max number of turns for trainer:"))
    move_generation = input("Move distribution (uniform, normal, side_biased):")

    if start_first > num_sessions or start_first < 0:
        ai_start = num_sessions
        trainer_start = 0
    else:
        ai_start = start_first
        trainer_start = num_sessions - ai_start

    who_starts = ["R"] * ai_start + ["Y"] * trainer_start
    session_data = []
    num_sessions_completed = 0
    print("\nRunning session...")
    session_start_time = time.time()
    while who_starts:
        starter = who_starts.pop()
        session_data.append(train_ai(starter, num_rounds, move_generation))

        num_sessions_completed += 1
        completion_rate = round((num_sessions_completed*100) / num_sessions, 1)
        fill_bars = int(completion_rate/4)
        print(f"{completion_rate}% complete |{'='*fill_bars + ' '*(25 - fill_bars)}|", end="")
        print("\r", end="")

    total_ai_playing_time = 0
    total_num_learned_moves = 0
    w, d, l = 0, 0, 0

    print("\n")
    for i in range(len(session_data)):
        total_num_learned_moves += session_data[i][0]
        total_ai_playing_time += session_data[i][1]
        if session_data[i][2] == "W":
            w += 1
        elif session_data[i][2] == "D":
            d += 1
        elif session_data[i][2] == "L":
            l += 1

    total_session_time = time.time() - session_start_time

    print(f"FULL SESSION SUMMARY")
    print(f"Total number of moves learned: {total_num_learned_moves} moves")
    print(f"Total AI playing time: {round(total_ai_playing_time, 3)} seconds")
    print(f"Total Session time: {round(total_session_time, 3)} seconds")
    print(f"Number of rounds played each game: {num_rounds} rounds")
    print(f"Win rate: {round((w*100)/num_sessions, 1)}%")
    print(f"Draw rate: {round((d*100)/num_sessions, 1)}%")
    print(f"Loss rate: {round((l*100)/num_sessions, 1)}%")
    print("\n")


def train_ai(ai="R", rounds=10, move_generation="normal"):
    y, r = "🟡", "🔴"

    num_learned_moves = 0
    total_ai_time_spent = 0
    game_status = "D"
    trainer_turns_played = 0

    board = create_board()
    current_player = r

    if ai == "R":
        ai = r
        trainer = y
    else:
        ai = y
        trainer = r

    while not full_board(board) and not check_win(board)[0] and trainer_turns_played < rounds:
        if current_player == trainer:
            user_input = generate_move(board, move_generation)
            trainer_turns_played += 1

        elif current_player == ai:
            start = time.time()
            ai_move, new_state = alpha_beta_search(board, current_player)
            time_spent = time.time() - start
            total_ai_time_spent += time_spent
            user_input = ai_move[1]

            if new_state:
                num_learned_moves += 1

        board = make_move(board, current_player, user_input)
        if check_win(board)[0]:
            if current_player == ai:
                game_status = "W"
            else:
                game_status = "L"

        if current_player == r:
            current_player = y
        elif current_player == y:
            current_player = r

    return num_learned_moves, total_ai_time_spent, game_status


if __name__ == "__main__":
    run_training_session()
