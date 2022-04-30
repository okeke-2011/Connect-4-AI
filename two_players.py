from game_play_helpers import *


def two_player():
    y, r = "🟡", "🔴"
    accepted_inputs = set([str(i) for i in range(1, 8)])
    board = create_board()
    current_player = r

    show_board(board)
    print("\n")

    while not full_board(board) and not check_win(board)[0]:
        print(f"\nPlayer {current_player}:")
        user_input = input(f"Select a column to play 1-7:")
        if user_input == "x":
            break

        elif user_input not in accepted_inputs:
            print(f"\nOnly numbers from 1-7 are allowed!")
            show_board(board)
            continue

        elif col_full(board, int(user_input)-1):
            print("\nYou can't play in a full column!")
            show_board(board)
            continue

        board = make_move(board, current_player, int(user_input)-1)
        show_board(board)

        if check_win(board)[0]:
            print(f"\nPlayer {current_player} wins!")
            show_win(board)
            print("\n")

        if current_player == r:
            current_player = y
        elif current_player == y:
            current_player = r

    if full_board(board) and not check_win(board)[0]:
        print("No one won :(")


if __name__ == "__main__":
    two_player()
