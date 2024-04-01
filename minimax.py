import math
import random
import time
import pygame
from Piece import update_sprite
from memory_profiler import profile

cuts = 0
explored = 0
totalT = 0.0
 
def minimax(state, depth, alpha, beta, maximizing, player, evaluate_func, only_longest,ab_cut):
    """Runs the Minimax algorithm from a given state and returns the best evaluation and corresponding state.
    Minimax parameters such as alpha, beta and depth are passed through recursion."""
    global cuts, explored
    explored +=  1
    winner = state.check_win()
    if depth == 0 or winner != 2:
        return evaluate_func(player, state), state
    
    
    counter = 0
    if maximizing:
        if only_longest:
            moves = state.get_all_moves(only_longest=True)
        else:
            moves = state.get_all_moves()
        maxEval = -math.inf
        best_move = None
        for move in moves:
            move.player = 1 - move.player
            counter += 1
            eval, _ = minimax(move, depth-1, alpha, beta, False, player, evaluate_func, only_longest,ab_cut)
            if (best_move == None or eval > maxEval):
                maxEval = eval
                best_move = move
                #if best_move == None or random.randint(0, 1):
                #    best_move = move
            
            if(ab_cut):
                alpha = max(alpha, maxEval)
                if beta <= alpha:
                    cuts += 1
                    break
        
        if counter == 0:
            return evaluate_func(player, state), state
        return maxEval, best_move
    else:
        moves = state.get_all_moves()
        minEval = math.inf
        best_move = None
        for move in moves:
            move.player = 1 - move.player
            counter += 1
            eval, _ = minimax(move, depth-1, alpha, beta, True, player, evaluate_func, only_longest,ab_cut)
            if (best_move == None or eval < minEval):
                minEval = eval
                best_move = move
                #if best_move == -1 or random.randint(0, 1):
                #    best_move = move
            if ab_cut:
                beta = min(beta, minEval)
                if beta <= alpha:
                    cuts += 1
                    break

        if counter == 0:
            return evaluate_func(player, state), state
        return minEval, best_move

def show_minimax_statistics(screen, font, first):
    """"Displays the statistics tied to the last execution of Minimax: the number of A-B cuts, how many nodes were explored, and execution time."""
    text = f"{cuts} A-B cuts, {explored} explored, {totalT:.3f} s"
    if first:
        print(text)
    display_text = font.render(text, True, (0,0,0))
    textRect = display_text.get_rect()
    textRect.topleft = (0, 0)
    screen.blit(display_text, textRect)
    pygame.display.flip()

def execute_minimax_move(state, evaluate_func, depth, only_longest=False,ab_cut=False):
    """Executes a minimax move from a given state with a given heuristic. If only_longest is set to True, the maximizing player will ignore short sequences.
    If ab_cut is set to True, Alpha-Beta pruning will not be performed."""
    global cuts, totalT, explored
    cuts = 0
    explored = 0
    startT = time.time()
    _, move = minimax(state, depth, -math.inf, math.inf, True, state.player, evaluate_func, only_longest,ab_cut)
    endT = time.time()
    totalT = endT-startT
    move.check_win()
    #move.player = not move.player
    return move
