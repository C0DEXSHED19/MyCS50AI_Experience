"""
Tic Tac Toe Player
"""
import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if terminal(board):
        return None
    else :
        x = 0
        o = 0
        for i in range(0,3):
            for j in range(0,3):
                v = board[i][j]
                if v == X:
                    x += 1
                elif v == O:
                    o += 1
                
        if x == 0 and o == 0:
            return X
        elif x == o:
            return X
        else:
            return O
    


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    if terminal(board):
        return None
    
    actions = set()
    for i in range(0,3):
        for j in range(0,3):
            if board[i][j] == EMPTY:
                actions.add((i,j))
                
    return actions
    


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("cannot make move!")
    else:
        b = copy.deepcopy(board)
        b[action[0]][action[1]] = player(board)
        return b
    


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    win = (None,None)
    if board[0][0] == board[0][1] and board[0][1] == board[0][2]:
        win = (0,0)
    elif board[1][0] == board[1][1] and board[1][1] == board[1][2]:
        win = (1,0)
    elif board[2][0] == board[2][1] and board[2][1] == board[2][2]:
        win = (2,0)
    elif board[0][0] == board[1][0] and board[1][0] == board[2][0]:
        win = (0,0)
    elif board[0][1] == board[1][1] and board[1][1] == board[2][1]:
        win = (0,1)
    elif board[0][2] == board[1][2] and board[1][2] == board[2][2]:
        win = (0,2)
    elif board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        win = (0,0)
    elif board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        win = (1,1)
        
    if win[0] == None:
        return None
    else:
        return board[win[0]][win[1]]


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    count = 0
    for i in range(0,3):
        for j in range(0,3):
            if board[i][j] == None:
                count += 1
            
    if winner(board) == None and count > 0:
        return False
    else:
        return True
    


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == None:
        return 0
    elif winner(board) == X:
        return 1
    else:
        return -1


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    else:
        if player(board) == X:
            util, move = OptimalX(board)
            return move
        else:
            util, move = OptimalO(board)
            return move
    
        
def OptimalX(board):
    if terminal(board):
        return utility(board), None
    else:
        max = -2       
        optimal_move = None
        for move in actions(board):
            r, n = OptimalO(result(board, move))
            if r > max:
                max = r
                optimal_move = move
                
        return max, optimal_move
    
def OptimalO(board):
    if terminal(board):
        return utility(board), None
    else:
        min = 2       
        optimal_move = None
        for move in actions(board):
            action = move
            r, n = OptimalX(result(board,move))
            if r < min:
                min = r
                optimal_move = action 
                
        return min, optimal_move
                
                
    