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
    return x < 0 or x >= ROWS or y < 0 or y >= COLS

def generate_neighbors(position):
    for dir in directions:
        temp = (position[0] + dir[0], position[1] + dir[1])
        yield [temp, (temp[0] + dir[0], temp[1] + dir[1])]

def heuristic2(player, state):
    score = 0

    for x in range(1, ROWS, 2):
        for y in range(1, COLS, 2):
            if state.board[x][y] == player:
                score += 2
    
    return heuristic1(player, state) + score