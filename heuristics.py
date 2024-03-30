import numpy
from main import ROWS, COLS
import math
from collections import deque

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

    for x in range(1, ROWS-1):
        for y in range(1, COLS-1):
            if x%2 == x%2:
                if state.board[x][y] == player and (not state.can_be_captured((x, y))):
                    score += 1
                elif state.board[x][y] == (not player):
                    score -= 1
    for x in range(0, ROWS, ROWS-1):
        for y in range(COLS):
            if state.board[x][y] == player:
                score -= 0.5
            elif state.board[x][y] == (not player):
                score += 0.5
    for x in range(ROWS):
        for y in range(0, COLS, COLS-1):
            if state.board[x][y] == player:
                score -= 0.5
            elif state.board[x][y] == (not player):
                score += 0.5
    
    return 5*heuristic1(player, state) + score

def dfs(board, player, x, y, count=0):
    board[x][y] = 2
    for i in range(4):
        new_x = x+directions[i][0]
        new_y = y+directions[i][1]
        if in_bounds((new_x, new_y)) and board[new_x][new_y] == player:
            count += dfs(board, player, x+directions[i][0], y+directions[i][1], count)

    return count

def bfs(board, sources, player):
    score = 0
    queue = deque()
    for source in sources:
        queue.append((source, 0))

    while len(queue) > 0:
        (x, y), value = queue.popleft()
        if board[x][y] == (not player):
            score += value
        board[x][y] = 3
        for i in range(4):
            new_x = x+directions[i][0]
            new_y = y+directions[i][1]
            if in_bounds((new_x, new_y)) and board[new_x][new_y] != 3:
                queue.append(((new_x, new_y), value + 1))

    return score
        

def heuristic3(player, state):
    chunks = 0
    board = state.board.copy()
    for x in range(ROWS):
        for y in range(COLS):
            if (board[x][y] == player):
                size = dfs(board, player, x, y)
                chunks += 1

    return heuristic2(player, state) - 0.5*chunks

def heuristic4(player, state):
    winner = state.check_win()
    if winner == player:
        return math.inf
    elif winner == (not player):       # or winner == -1:
        return -math.inf
    else:
        return heuristic3(player, state)
    
def heuristic5(player, state):
    score = 0
    for x in range(ROWS):
        for y in range(1 - x%2, COLS, 2):
            if state.board[x][y] == player and (not state.can_be_captured((x, y))):
                for nx in [-1,1]:
                    for ny in [-1,1]:
                        if in_bounds((nx, ny)) and state.board[nx][ny] == (not player):
                            score += 1
    
    for x in range(0, ROWS, ROWS-1):
        if x == 0:
            offset = 1
        else:
            offset = -1
        for y in range(1, COLS-1):
            if state.board[x][y] == (not player) and state.board[x+offset][y] == player:
                score += 1
    for x in range(1, ROWS-1):
        for y in range(0, COLS, COLS-1):
            if y == 0:
                offset = 1
            else:
                offset = -1
            if state.board[x][y] == (not player) and state.board[x][y+offset] == player:
                score += 1
    
    return heuristic4(player, state) + 0.5*score

def heuristic6(player, state):
    score = 0
    prev = heuristic5(player, state)
    if player == 1:
        enemy_pieces = state.black_pieces
        my_pieces = state.white_pieces
    else:
        enemy_pieces = state.white_pieces
        my_pieces = state.black_pieces

    if enemy_pieces < (ROWS*COLS//2)*0.25 and enemy_pieces <= my_pieces:
        sources = []
        for x in range(ROWS):
            for y in range(COLS):
                if state.board[x][y] == (not player):
                    sources.append((x, y))
        score = bfs(state.board.copy(), sources, player)
        prev += my_pieces*min(ROWS, COLS)
    
    return prev - score
    
    