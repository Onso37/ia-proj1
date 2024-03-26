import numpy
from main import ROWS, COLS

left = (0,-1)
right = (0, 1)
up = (-1,0)
down = (1,0)
up_left = (-1,-1)
up_right =(-1,1)
down_left = (1,-1)
down_right = (1,1)
directions = [left, right, up, down, up_left, up_right, down_left, down_right]

def heuristic1(player, state):
    if player == 1:
        return state.white_pieces - state.black_pieces
    else:
        return state.black_pieces - state.white_pieces
    #count_a = numpy.count_nonzero(state.board == player)
    #count_b = numpy.count_nonzero(state.board == (not player))
    #return count_a - count_b

def in_bounds(position):
    x, y = position
    return not (x < 0 or x >= ROWS or y < 0 or y >= COLS)

def generate_neighbors(position):
    for dir in directions:
        temp = (position[0] + dir[0], position[1] + dir[1])
        yield [temp, (temp[0] + dir[0], temp[1] + dir[1])]

def heuristic2(player, state):
    score = 0

    for x in range(1, ROWS, 2):
        for y in range(1, COLS, 2):
            if state.board[x][y] == player:
                score += 1
    
    return 5*heuristic1(player, state) + score

def dfs(board, player, x, y):
    board[x][y] = 2
    for i in range(4):
        new_x = x+directions[i][0]
        new_y = y+directions[i][1]
        if in_bounds((new_x, new_y)) and board[new_x][new_y] == player:
            dfs(board, player, x+directions[i][0], y+directions[i][1])
        

def heuristic3(player, state):
    chunks = 0
    board = state.board.copy()
    for x in range(ROWS):
        for y in range(COLS):
            if (board[x][y] == player):
                dfs(board, player, x, y)
                chunks += 1

    return heuristic2(player, state) - 0.5*chunks