# Connect-4-AI
## Brief overview
I coded up the Connect-4 (or four-in-a-row) game in python with two players. I then replace one of the players with a game-playing AI that uses the minimax algorithm to make moves.
## Minimax?
The core of this algorithm is the assumption of optimal play between two rational players trying to maximize a utility function. To determine an optimal move, the AI works down to the end of the game tree (terminal state) and picks the option that will give the highest utility despite the other player's efforts. For Connect-4, working out the game tree is infeasible. Hence, I work down the game tree to some depth (set to 5 in the code) and use an evaluation function to decide the best move. 
## My Evaluation Function
The evaluation function basically gives a score based on how good a position you are in relative to your opponent. I built my evaluation function based on how many three and two-in-a-row chances the player has, with more weight on the three-in-a-row chances. 
