import time

from minimax_algorithm import *


def play_ai(ai = "R"):
    y, r = "🟡", "🔴"
    accepted_inputs = set([str(i) for i in range(1, 8)])
    board = create_board()
    utils = {"-1000":"DAMN! If you're careful, I might actually lose :(",
             "0":"This could go either way.",
             "1000":"Lol dude, you're screwed :)"
            }
    current_player = r
    
    if ai == "R":
        ai = r
        human = y
    else:
        ai = y
        human = r
    
    show_board(board)
    print("\n")
    
    while not full_board(board) and not check_win(board)[0]:
        print(f"\nPlayer {current_player}:")
        
        if current_player == human:
            user_input = input(f"Select a column to play 1-7:")
            if user_input == "x":
                break

            elif user_input not in accepted_inputs:
                print(f"\nOnly numbers from 1-7 are allowed!")
                show_board(board)
                continue

            elif col_full(board, int(user_input) - 1):
                print("\nYou can't play in a full column!")
                show_board(board)
                continue

            else:
                user_input = int(user_input) - 1
            
        elif current_player == ai:
            start = time.time()
            ai_move, new_state = alpha_beta_search(board, current_player)
            time_spent = time.time() - start
            
            if str(ai_move[0]) in utils.keys():
                print(f"AI: {utils[str(ai_move[0])]}")
            else:
                print(f"AI: Move utility = {ai_move[0]/1000:.3f}")
                
            print(f"AI took {time_spent:.3f} seconds")
            user_input = ai_move[1]
    
        board = make_move(board, current_player, user_input)
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
    human_start = input("Would you like to go first (Y/N)?")
    if human_start in ["Y", "y"]:
        play_ai("Y")
    elif human_start in ["N", "n"]:
        play_ai("R")
    else:
        print("Invalid input! AI will start...")
        play_ai("R")


