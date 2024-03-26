import math
import random
import numpy
from Piece import update_sprite
import collections

def minimax(state, depth, alpha, beta, maximizing, player, evaluate_func):
    if depth == 0:
        return evaluate_func(player, state), state
    
    moves = state.get_all_moves()
    counter = 0
    if maximizing:
        maxEval = -math.inf
        best_move = None
        for move in moves:
            counter += 1
            eval, _ = minimax(move, depth-1, alpha, beta, False, player, evaluate_func)
            if (eval >= maxEval):
                maxEval = eval
                best_move = move
                #if best_move == None or random.randint(0, 1):
                #    best_move = move
            alpha = max(alpha, maxEval)

            if beta <= alpha:
                break
        
        if counter == 0:
            return evaluate_func(player, state), state
        return maxEval, best_move
    else:
        minEval = math.inf
        best_move = None
        for move in moves:
            counter += 1
            eval, _ = minimax(move, depth-1, alpha, beta, True, player, evaluate_func)
            if (eval <= minEval):
                minEval = eval
                best_move = move
                #if best_move == -1 or random.randint(0, 1):
                #    best_move = move
            beta = min(beta, minEval)

            if beta <= alpha:
                break

        if counter == 0:
            return evaluate_func(player, state), state
        return minEval, best_move

def heuristic1(player, state):
    count_a = numpy.count_nonzero(state.board == player)
    count_b = numpy.count_nonzero(state.board == (not player))
    return count_a - count_b


def execute_minimax_move(screen, font, state, pieces):
    _, move = minimax(state, 2, -math.inf, math.inf, True, state.player, heuristic1)
    winner = move.check_win()
    move.player = not move.player
    pieces = update_sprite(move, screen)
    return move, pieces
