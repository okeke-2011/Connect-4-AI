#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np
import matplotlib.pyplot as plt
import copy
import time


# In[4]:


y, r, w = "🟡", "🔴", "⚪️"

def create_board():
    return [["⚪️" for i in range(7)] for i in range(6)]

def show_board(board):
    template = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣"]
            
    print("\nCurrent Board State:")
    print(template)
    for i in range(len(board)):
        print(board[i])
        print("-------------------------------------------")
        
def get_diagonals(board, bltr = True):
    return_grid = [[] for total in range(12)]
    for i in range(7):
        for j in range(6):
            if bltr: 
                return_grid[i+j].append(board[j][i])
            else:  
                return_grid[(j-i)%12].append(board[j][i])
    return return_grid

def retrieve_diagonal(ind):
    lst = []
    if ind < 12:
        for i in range(7):
            for j in range(6):
                if i+j == ind:
                    lst.append([j,i])
    elif ind >= 12:
        ind = ind - 12
        for i in range(7):
            for j in range(6):
                if (j-i)%12 == ind:
                    lst.append([j,i])
    return lst


# In[5]:


def check_win(board):
    y, r, w = "🟡", "🔴", "⚪️"
    
    diagonals = get_diagonals(board) + get_diagonals(board, False)
    # check diagonals 
    for ind, diagonal in enumerate(diagonals):
        if len(diagonal) >= 4:
            for i in range(len(diagonal)-3):
                if diagonal[i:i+4] == [r for i in range(4)]:
                    return True, r, retrieve_diagonal(ind)[i:i+4]
                if diagonal[i:i+4] == [y for i in range(4)]:
                    return True, y, retrieve_diagonal(ind)[i:i+4]
    
    # check rows 
    for ind, row in enumerate(board):
        for i in range(4):
            if row[i:i+4] == [r for i in range(4)]:
                return True, r, [[ind,i+j] for j in range(4)]
            if row[i:i+4] == [y for i in range(4)]:
                return True, y, [[ind,i+j] for j in range(4)]
    
    # check columns
    board_t = np.transpose(np.array(board))
    for ind, col in enumerate(board_t):
        for i in range(3):
            if list(col)[i:i+4] == [r for i in range(4)]:
                return True, r, [[i+j,ind] for j in range(4)]
            if list(col)[i:i+4] == [y for i in range(4)]:
                return True, y, [[i+j,ind] for j in range(4)]
    
    return False, None, None

def show_win(board):
    win, player, pos = check_win(board)
    dummy = copy.deepcopy(board)
    
    if win:
        for row, col in pos:
            dummy[row][col] = "✅"
    show_board(dummy)


# In[6]:


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
        for i in range(5,-1,-1):
            if dummy[i][col] == w:
                dummy[i][col] = player
                break
        return dummy
    else:
        return dummy

def possible_moves(board):
    y, r, w = "🟡", "🔴", "⚪️"
    moves = []
    for col in range(7):
        if not col_full(board, col):
            moves.append(col)
    return moves


# In[9]:


def two_player():
    y, r = "🟡", "🔴"
    board = create_board()
    current_player = r
    
    show_board(board)
    print("\n")
    
    while not full_board(board) and not check_win(board)[0]:
        print(f"\nPlayer {current_player}:")
        user_input = int(input(f"Select a column to play 1-7:"))-1
            
        if user_input > 6 or user_input < 0:
            print(f"\nOnly numbers from 1-7 are allowed!")
            show_board(board)
            continue
        
        if col_full(board, user_input):
            print("\nYou can't play in a full column!")
            show_board(board)
            continue
    
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
    
# two_player()


# In[11]:


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


# In[12]:


def eval_func(board, player):
    y, r, w = "🟡", "🔴", "⚪️"
    Y, R = [0 for i in range(3)], [0 for i in range(3)]
    
    if is_terminal(board):
        return utility(board, player)
    
    diags = [d for d in get_diagonals(board)+get_diagonals(board,False) if len(d)>=4]
    board_t = np.transpose(np.array(board))
    all_4 = []
    
    for row in board:
        for i in range(len(row)-3):
            all_4.append(row[i:i+4])
    
    for col in board_t:
        for i in range(len(col)-3):
            all_4.append(list(col)[i:i+4])
    
    for diag in diags:
        for i in range(len(diag)-3):
            all_4.append(diag[i:i+4])
            
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
        return 9*R[2] + 3*R[1] + R[0] - (9*Y[2] + 3*Y[1] + Y[0])
    else:
        return 9*Y[2] + 3*Y[1] + Y[0] - (9*R[2] + 3*R[1] + R[0])


# In[13]:


def memoize_search(search):
    memory = {}
    def inner(board, player):
        if str(board)+player not in memory:         
            memory[str(board)+player] = search(board, player)
        return memory[str(board)+player]
  
    return inner


# In[14]:


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
            v2, a2 = min_value(new_board, alpha, beta, current_player, depth+1, max_depth)
        
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
            v2, a2 = max_value(new_board, alpha, beta, current_player, depth+1, max_depth)
        
        if v2 < v:
            v, move = v2, a
            beta = min(beta, v)
        
        if v <= alpha:
            return v, move
    return v, move


# In[16]:


def play_ai(ai = "R"):
    y, r = "🟡", "🔴"
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
            user_input = int(input(f"Select a column to play 1-7:"))-1
            
        elif current_player == ai:
            start = time.time()
            ai_move = alpha_beta_search(board, current_player)
            time_spent = time.time() - start
            
            if str(ai_move[0]) in utils.keys():
                print(f"AI: {utils[str(ai_move[0])]}")
            else:
                print(f"AI: Move utility = {ai_move[0]/1000:.3f}")
                
            print(f"AI took {time_spent:.3f} seconds")
            user_input = ai_move[1]
            
        if user_input > 6 or user_input < 0:
            print(f"\nOnly numbers from 1-7 are allowed!")
            show_board(board)
            continue
        
        if col_full(board, user_input):
            print("\nYou can't play in a full column!")
            show_board(board)
            continue
    
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
    
# play_ai("Y")


# In[17]:


y, r, w = "🟡", "🔴", "⚪️"

# np.random.seed(123)
hey = create_board()
for i in range(20):
    move = np.random.choice(possible_moves(hey))
    player = np.random.choice([y,r])
    hey = make_move(hey, player, move)

# hey = make_move(hey, r, 1)
# hey = make_move(hey, r, 2)
# hey = make_move(hey, r, 3)
# hey = make_move(hey, y, 2)
# hey = make_move(hey, y, 2)
# hey = make_move(hey, y, 2)
# hey = make_move(hey, r, 1)

# show_board(hey)

# print("\n")

# show_win(hey)


# In[ ]:




