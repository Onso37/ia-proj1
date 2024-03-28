import math
import random
import time
import pygame
import numpy
from Piece import update_sprite
import collections

cuts = 0
totalT = 0.0

def minimax(state, depth, alpha, beta, maximizing, player, evaluate_func):
    global cuts
    if depth == 0:
        return evaluate_func(player, state), state
    
    moves = state.get_all_moves()
    counter = 0
    if maximizing:
        maxEval = -math.inf
        best_move = None
        for move in moves:
            move.player = not move.player
            counter += 1
            eval, _ = minimax(move, depth-1, alpha, beta, False, player, evaluate_func)
            if (eval >= maxEval):
                maxEval = eval
                best_move = move
                #if best_move == None or random.randint(0, 1):
                #    best_move = move
            alpha = max(alpha, maxEval)

            if beta <= alpha:
                cuts += 1
                break
        
        if counter == 0:
            return evaluate_func(player, state), state
        return maxEval, best_move
    else:
        minEval = math.inf
        best_move = None
        for move in moves:
            move.player = not move.player
            counter += 1
            eval, _ = minimax(move, depth-1, alpha, beta, True, player, evaluate_func)
            if (eval <= minEval):
                minEval = eval
                best_move = move
                #if best_move == -1 or random.randint(0, 1):
                #    best_move = move
            beta = min(beta, minEval)

            if beta <= alpha:
                cuts += 1
                break

        if counter == 0:
            return evaluate_func(player, state), state
        return minEval, best_move

def show_statistics(screen, font):
    display_text = font.render(f"{cuts} A-B cuts, {totalT} s", True, (0,0,0))
    textRect = display_text.get_rect()
    textRect.topleft = (0, 0)
    screen.blit(display_text, textRect)
    pygame.display.flip()

def execute_minimax_move(state, evaluate_func):
    global cuts, totalT
    cuts = 0
    startT = time.time()
    _, move = minimax(state, 4, -math.inf, math.inf, True, state.player, evaluate_func)
    endT = time.time()
    totalT = endT-startT
    move.check_win()
    #move.player = not move.player
    return move
