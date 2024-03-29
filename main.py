# import the pygame module, so you can use it
import pygame
import numpy
import time
from Piece import *
from mcts import execute_mcts_move, show_mcts_statistics
from AIPlayer import *
from heuristics import *
import random
import functools 
from minimax import execute_minimax_move, show_minimax_statistics
from copy import deepcopy
from collections import deque


capture_by_approach=0
capture_by_withdrawal=1
no_capture=-1


player_turn = white  #white starts
left = (0,-1)
right = (0, 1)
up = (-1,0)
down = (1,0)
up_left = (-1,-1)
up_right =(-1,1)
down_left = (1,-1)
down_right = (1,1)
directions = [left, right, up, down, up_left, up_right, down_left, down_right]
displayed = False

ROWS = 5
COLS = 9

GUI = False

def turn_change():
    global player_turn
    player_turn = not player_turn
    
def manage_gamestate(self_piece,enemy_piece):
    global displayed
    if(player_turn == white and self_piece.isWhite):
        if(enemy_piece.isWhite and not enemy_piece.isWhite == space):
            print("Invalid move")
            return -1
        turn_change()
        displayed = False
    elif (player_turn==black and not self_piece.isWhite):
        if(not enemy_piece.isWhite and not enemy_piece.isWhite == space):
            print("Invalid move")
            return -1
        turn_change()
        displayed = False
    else:
        print("Not your turn")
        return -1
    return 0
def is_even(x):
    return x%2==0
def is_diagonal(x1,y1,x2,y2):
    return abs(x1-x2) == abs(y1-y2)
def vector_sum(v1,v2):
    return (v1[0]+v2[0],v1[1]+v2[1])
def vector_sub(v1,v2):
    return (v1[0]-v2[0],v1[1]-v2[1])
def is_same_orientation(vector1, vector2):
    if(vector1[0]==0 and vector1[1]!=0):
        declive1 = None
    else:
        declive1 = vector1[1] / vector1[0]
    if(vector2[0]==0 and vector2[1]!=0):
        declive2 = None
    else:
        declive2 = vector2[1] / vector2[0]
    return declive1 == declive2

class State:
    def __init__(self):
        self.board = numpy.zeros((ROWS,COLS))
        self.player = 1
        self.capture = no_capture
        self.last_dir = None
        self.capture_positions = []
        self.white_pieces = (ROWS * COLS)//2
        self.black_pieces = (ROWS * COLS)//2
        self.white_captured = 0
        self.black_captured = 0
        self.non_captures = 0
        self.available_moves = [(ROWS//2,COLS//2)]
        self.moved_pos = []
        self.boards = []
        self.winner = 2 #2 no winner, 0 for black, 1 for white, -1 for no winner
        for y in range(COLS):
            for x in range(ROWS//2):
                self.board[x][y] = black
        for y in range(COLS//2):
            if(y%2==0):
                self.board[ROWS//2][y] = black
            else:
                self.board[ROWS//2][y] = white
        for y in range((COLS//2) + 1, COLS):
            if(y%2==0):
                self.board[ROWS//2][y] = white
            else:
                self.board[ROWS//2][y] = black
        
        for y in range(COLS):
            for x in range((ROWS//2)+1, ROWS):
                self.board[x][y] = white
        self.board[ROWS//2][COLS//2] = space
    def has_diagonal(self,player_pos,move):
        xi,yi=player_pos
        x,y = move
        if(is_diagonal(xi,yi,x,y)):
            if((is_even(xi) and is_even(yi)) or (not is_even(xi) and not is_even(yi))):
                return True
        return False
    def possible_move(self,player_pos,move):
        xi,yi=player_pos
        x,y = move
        xf,yf = x-xi,y-yi
        
        if (x < 0 or x >= ROWS or y < 0 or y >= COLS):
            return False
        if(abs(xf)>1 or abs(yf)>1):
            return False
        if(self.player != self.board[xi][yi] ): 
            return False
        if(is_diagonal(xi,yi,x,y)):
            if((is_even(xi) and is_even(yi)) or (not is_even(xi) and not is_even(yi))):
                if(self.board[x][y] == space):
                    return True
        else:
            if(self.board[x][y] == space):
                return True

        return False
    
    def possible_moves(self,player_pos,move,previous_state=None):
    
        temp_avalable_moves = list()
        eval_vec=(move[0]-player_pos[0],move[1]-player_pos[1])
        

        for dir in directions:
            if self.possible_move(move, vector_sum(move, dir)) and (not is_same_orientation(eval_vec,dir)):
                temp_avalable_moves.append(vector_sum(move, dir))
        
        temp_avalable_moves = [m for m in temp_avalable_moves if ((self.evaluate_capture(move,m)[0] or self.evaluate_capture(move,m)[1]) and (m not in previous_state.moved_pos))]
        
            
        
        print(temp_avalable_moves)
        return temp_avalable_moves
    
    def possible_moves_2(self, x, y):
        moves = []
        for dir in directions:
            if self.possible_move((x,y), vector_sum((x, y), dir)):
                moves.append(dir)
        return moves

    
    def evaluate_capture(self,player_pos,move):
        xi,yi=player_pos
        x,y = move
        captures=numpy.zeros(2)
        vector = (0,0)
        if((x-xi)==0 and (y-yi)!= 0):
          vector = (0,(y-yi)//abs(y-yi))
        elif((x-xi)!=0 and (y-yi)==0):
          vector = ((x-xi)//abs(x-xi),0)
        elif((x-xi)==0 and (y-yi)==0):
          vector = (0,0)
        else:
          vector = ((x-xi)//abs(x-xi),(y-yi)//abs(y-yi))
        withdrawal = vector_sum(player_pos,(-vector[0],-vector[1]))
        approach = vector_sum(move,vector)
        
        if ((withdrawal[0] >= 0 and withdrawal[0] < ROWS) and (withdrawal[1] >= 0 and withdrawal[1] < COLS)):
            if(self.board[withdrawal[0]][withdrawal[1]] == (not self.player) and self.board[withdrawal[0]][withdrawal[1]] != space):
                captures[capture_by_withdrawal] = True
        if ((approach[0] >= 0 and approach[0] < ROWS) and (approach[1] >= 0 and approach[1] < COLS) and self.board[approach[0]][approach[1]] != space):
            if( self.board[approach[0]][approach[1]] == (not self.player) ):
                captures[capture_by_approach] = True
        return captures
            
    def capture_move(self,player_pos,move):
        xi,yi=player_pos
        x,y = move
        vector = (0,0)
        if((x-xi)==0 and (y-yi)!= 0):
          vector = (0,(y-yi)//abs(y-yi))
        elif((x-xi)!=0 and (y-yi)==0):
          vector = ((x-xi)//abs(x-xi),0)
        elif((x-xi)==0 and (y-yi)==0):
          vector = (0,0)
        else:
          vector = ((x-xi)//abs(x-xi),(y-yi)//abs(y-yi))
        
        self.board[x][y] = self.player
        self.board[xi][yi] = space
        if(self.capture == capture_by_approach):
            temp = vector_sum(move,vector)
            while(temp[0]>=0 and temp[0]<ROWS and temp[1]>=0 and temp[1]<COLS):
                if(self.board[temp[0]][temp[1]] != self.player and self.board[temp[0]][temp[1]] != space):
                    if(self.player==white):
                        self.black_captured += 1
                        self.black_pieces -= 1
                    else:
                        self.white_captured += 1
                        self.white_pieces -= 1  
                    self.board[temp[0]][temp[1]] = space
                    temp = vector_sum(temp,vector)
                else:
                    break
            return move
        elif(self.capture == capture_by_withdrawal):
            vector = (-vector[0],-vector[1])
            temp = vector_sum(player_pos,vector)
            while(temp[0]>=0 and temp[0]<ROWS and temp[1]>=0 and temp[1]<COLS):
                if(self.board[temp[0]][temp[1]] != self.player and self.board[temp[0]][temp[1]] != space):
                    if(self.player==white):
                        self.black_captured += 1
                        self.black_pieces -= 1
                    else:
                        self.white_captured += 1
                        self.white_pieces -= 1  
                    self.board[temp[0]][temp[1]] = space
                    temp = vector_sum(temp,vector)
                else:
                    break
            return move
        
        return -1
    
        
    def move(self,player_pos,move,screen,font):
        global displayed
        displayed = False
        xi,yi=player_pos
        x,y = move
        state_copy = deepcopy(self)

        if(self.possible_move(player_pos,move)):
            print(self.available_moves)
            captures = self.evaluate_capture(player_pos,move)
            if(captures[0] and captures[1]):
                #choice=input("Enter 1 for approach, 2 for withdrawal\n")
                choice=get_pygame_input(screen, font, ["Approach", "Withdrawal"])
                if(choice==1):
                    state_copy.capture = capture_by_approach
                else:
                    state_copy.capture = capture_by_withdrawal
                
            elif(captures[0]):
                state_copy.capture = capture_by_approach
            elif(captures[1]):
                state_copy.capture = capture_by_withdrawal
            else:
                state_copy.capture = no_capture
            print(state_copy.capture)
            state_copy.capture_move(player_pos,move)
            state_copy.board[x][y] = self.board[xi][yi]
            state_copy.board[xi][yi] = space
            state_copy.available_moves = state_copy.possible_moves(player_pos,move,self)
            state_copy.check_win() 
            #case has capture    
            if(state_copy.capture != no_capture):
                if(state_copy.available_moves!=[]):
                    #choice = input("Enter 1 to continue capturing, 2 to end turn\n")
                    choice = get_pygame_input(screen, font, ["Continue capturing", "End turn"])
                    if(choice == 1):                            
                            state_copy.player = self.player
                            state_copy.moved_pos.append(player_pos)
                    else:
                        state_copy.moved_pos = []
                        state_copy.player = not self.player
                else:
                    print("No more moves for succesive capture")
                    state_copy.capture = no_capture
                    state_copy.player = not self.player
                    state_copy.moved_pos = []
            else:
                print("here")
                if(state_copy.available_moves == [] and (self.capture != no_capture)):
                    if(self.available_moves!=[]):
                        print("Invalid Move")
                        return -1
                    state_copy.player = not self.player
                    
                elif (self.available_moves == [] and (self.capture == no_capture) and (state_copy.available_moves != [] or state_copy.available_moves==[])):
                    print("First movement")
                    state_copy.moved_pos.append(player_pos)
                    state_copy.player = not self.player
                elif (self.capture!=no_capture):
                    print("Invalid Move")
                    return -1
                
                
                
            return state_copy
           

        else:
            print("Invalid move")
            return -1
    
    def in_bounds(self, x, y):
        return not (x < 0 or x >= ROWS or y < 0 or y >= COLS)

    def try_moves_bfs(self, x, y, in_sequence=False):
        #states = []
        global GUI
        queue = deque()
        longest_moves = []
        old_level = 0
        queue.append((self, False, (x,y), 1))
        while len(queue) > 0:
            state, in_sequence, (x,y), level = queue.popleft()
            if not in_sequence:
                state.last_dir = None
                state.capture_positions = [(x, y)]
            else:
                #states.append(self)
                state.check_win()
                if level != old_level:
                    old_level = level
                    longest_moves = [state]
                else:
                    longest_moves.append(state)
                yield state
            
            for dir in state.possible_moves_2(x, y):
                moved_pos = vector_sum((x, y), dir)
                if state.in_bounds(moved_pos[0], moved_pos[1]) and state.board[moved_pos[0], moved_pos[1]] != space:
                    continue

                if in_sequence and (dir == state.last_dir or moved_pos in state.capture_positions):
                    continue

                front_x, front_y = vector_sum(moved_pos, dir)
                back_x, back_y = vector_sub((x, y), dir)

                if state.in_bounds(front_x, front_y) and state.board[front_x][front_y] == (not state.player):
                    state_copy = deepcopy(state)
                    state_copy.capture = capture_by_approach
                    state_copy.last_dir = dir
                    state_copy.capture_positions.append(moved_pos)
                    if GUI:
                        state_copy.boards.append(state.board)
                    state_copy.non_captures=0

                    state_copy.capture_move((x, y), moved_pos)
                    queue.append((state_copy, True, moved_pos, level+1))
                    #yield from state_copy.try_moves(moved_pos[0], moved_pos[1], True)

                if self.in_bounds(back_x, back_y) and state.board[back_x][back_y] == (not state.player):
                    state_copy = deepcopy(state)
                    state_copy.capture = capture_by_withdrawal
                    state_copy.last_dir = dir
                    state_copy.capture_positions.append(moved_pos)
                    if GUI:
                        state_copy.boards.append(state.board)
                    state_copy.non_captures=0

                    state_copy.capture_move((x, y), moved_pos)
                    queue.append((state_copy, True, moved_pos, level+1))
                    #yield from state_copy.try_moves(moved_pos[0], moved_pos[1], True)
        #yield from longest_moves

    def try_moves(self, x, y, in_sequence=False):
        global GUI
        #states = []
        if not in_sequence:
            self.last_dir = None
            self.capture_positions = [(x, y)]
        else:
            #states.append(self)
            self.check_win()
            yield self
        
        for dir in self.possible_moves_2(x, y):
            moved_pos = vector_sum((x, y), dir)
            if self.in_bounds(moved_pos[0], moved_pos[1]) and self.board[moved_pos[0], moved_pos[1]] != space:
                continue

            if in_sequence and (dir == self.last_dir or moved_pos in self.capture_positions):
                continue

            front_x, front_y = vector_sum(moved_pos, dir)
            back_x, back_y = vector_sub((x, y), dir)

            if self.in_bounds(front_x, front_y) and self.board[front_x][front_y] == (not self.player):
                state_copy = deepcopy(self)
                state_copy.capture = capture_by_approach
                state_copy.last_dir = dir
                state_copy.capture_positions.append(moved_pos)
                if GUI:
                    state_copy.boards.append(self.board)
                state_copy.non_captures=0

                state_copy.capture_move((x, y), moved_pos)
                yield from state_copy.try_moves(moved_pos[0], moved_pos[1], True)

            if self.in_bounds(back_x, back_y) and self.board[back_x][back_y] == (not self.player):
                state_copy = deepcopy(self)
                state_copy.capture = capture_by_withdrawal
                state_copy.last_dir = dir
                state_copy.capture_positions.append(moved_pos)
                if GUI:
                    state_copy.boards.append(self.board)
                state_copy.non_captures=0

                state_copy.capture_move((x, y), moved_pos)
                yield from state_copy.try_moves(moved_pos[0], moved_pos[1], True)
                
    def try_non_captures(self, x, y):

        for dir in self.possible_moves_2(x, y):
            moved_pos = vector_sum((x, y), dir)
            if self.in_bounds(moved_pos[0], moved_pos[1]) and self.board[moved_pos[0], moved_pos[1]] != space:
                continue

            state_copy = deepcopy(self)
            state_copy.capture = no_capture
            state_copy.board[x][y] = space
            state_copy.non_captures+=1
            state_copy.board[moved_pos[0]][moved_pos[1]] = self.player
            state_copy.check_win()
            yield state_copy



    def get_available_captures(self):
        for x in range(ROWS):
            for y in range(COLS):
                if self.board[x][y] == self.player:
                    yield from self.try_moves_bfs(x, y)
    
    def get_available_non_captures(self):
        for x in range(ROWS):
            for y in range(COLS):
                if self.board[x][y] == self.player:
                    yield from self.try_non_captures(x, y)
    
    def get_all_moves(self):
        if self.check_win() != 2:
            yield from []
        counter = 0
        for move in self.get_available_captures():
            counter += 1
            yield deepcopy(move)

        if counter == 0:
            for move in self.get_available_non_captures():
                yield deepcopy(move)

    def check_win(self):
        if self.white_pieces == 0:
            self.winner = black
        elif self.black_pieces == 0:
            self.winner = white
        elif self.non_captures >= 10:
            self.winner = -1
        else:
            self.winner = 2
        return self.winner

        

def pygame_get_enter():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return 0
 
def draw_motif(screen, x, y, size):
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y, size, size), width=1)
    pygame.draw.line(screen, (0, 0, 0), (x+size/2, y), (x+size/2, y+size))
    pygame.draw.line(screen, (0, 0, 0), (x, y+size/2), (x+size, y+size/2))
    pygame.draw.line(screen, (0, 0, 0), (x, y), (x+size, y+size))
    pygame.draw.line(screen, (0, 0, 0), (x, y+size), (x+size, y))

def announce_winner(winner,screen,font):
    global GUI

    string_winner=""
    if(winner==1):
        string_winner="White wins"
    elif(winner==0):
        string_winner="Black wins"
    else:
        string_winner="Draw"
    if GUI:
        display_text = font.render(string_winner, True, (0,0,0))
        textRect = display_text.get_rect()
        textRect.bottomleft = (0, 480-24)
        screen.blit(display_text, textRect)
        pygame.display.flip()
        pygame_get_enter()
        return
    
    print(string_winner)
    
def draw_bg(screen):
    screen.fill((255, 255, 255))
    for x in range(COLS//2):
        for y in range(ROWS//2):
            draw_motif(screen, 128 + 96*x, 96*(y+1), 96)

def get_pygame_input(screen, font, opts):
    global GUI
    opts = list(map(lambda num, opt: f"{num}: {opt}", range(1, len(opts)+1), opts))

    print(GUI)
    if GUI == False:
        for opt in opts:
            print(opt)
        while True:
            val = int(input())
            if val >= 1 and val <= len(opts):
                return val
    
    for i in range(len(opts)):
        display_text = font.render(opts[len(opts)-i-1], True, (0,0,0))
        textRect = display_text.get_rect()
        textRect.bottomleft = (0, 480-24*i)
        screen.blit(display_text, textRect)
    pygame.display.flip()
    pygame.event.clear()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                if key >= '1' and key <= str(len(opts)):
                    rect = pygame.rect.Rect(0, 480-24*(len(opts)), 640, 24*(len(opts)))
                    screen.fill((255,255,255, 255), rect=rect)
                    pygame.display.flip()
                    return int(key)

def execute_player_move(screen, font, state, pieces):
    dragging = None
    running = True
    while running:
        draw_bg(screen)
        #pieces = update_sprite(state,screen)
        pieces.update()
        pieces.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not dragging:
                for piece in pieces:
                    if piece.rect.collidepoint(pygame.mouse.get_pos()):
                        dragging = piece
                        piece.dragging = True
            if event.type == pygame.MOUSEBUTTONUP and dragging:
                temp = state
                next_state= dragging.place(pygame.mouse.get_pos(),state, screen, font)
                if(next_state != -1):
                    state = next_state
                else:
                    state = temp
                pieces = update_sprite(state.board,screen,ROWS,COLS)
                dragging = None
                return state
            if event.type == pygame.MOUSEMOTION and dragging:
                dragging.drag(pygame.mouse.get_pos())

def execute_random_move(state, _):
    moves = state.get_all_moves()
    move = random.choice(list(moves))
    move.player = not move.player
    return move

# define a main function
def main():
    global GUI


    useGUI = get_pygame_input(None, None, ["With GUI", "Without GUI"])
    print(useGUI)
    if (useGUI == 1):
        GUI = True
    
    if not GUI:
        games = int(input("How many games?"))
    else:
        games = 1

    first = True
    players = [None, None]
    playerTypes = None
    for _ in range(games):
        state = State()
        if GUI:
            #test = state.get_all_moves()

            pygame.init()
            pygame.display.set_caption("Fanorona")
            font = pygame.font.Font(pygame.font.get_default_font(), 24)
            
            # create a surface on screen that has the size of 640 x 480
            screen = pygame.display.set_mode((640,480))
            pieces=update_sprite(state.board,screen,ROWS,COLS)
            draw_bg(screen)
            pieces.update()
            pieces.draw(screen)
            pygame.display.flip()
        else:
            screen = None
            font = None
            pieces = None

        running = True
        
        global displayed
        
        if GUI and first:
            mode = get_pygame_input(screen, font, ["Human vs Human", "Human vs AI", "AI vs Human", "AI vs AI"])
        else:
            mode = 4
        
        if first:
            match mode:
                case 1:
                    playerTypes = (1, 1)
                case 2:
                    playerTypes = (2, 1)
                case 3:
                    playerTypes = (1, 2)
                case 4:
                    playerTypes = (2, 2)

            algos = [execute_random_move, execute_minimax_move, execute_mcts_move]
            statistics = [None, show_minimax_statistics, show_mcts_statistics]
            difficulties = [heuristic1, heuristic2, heuristic3, heuristic4]
            for i in range(2):
                if playerTypes[i] == 2:
                    algoTypes = ["Random move", "Minimax", "Monte Carlo Tree Search"]
                    algo = get_pygame_input(screen, font, algoTypes) - 1
                    if algo == 1:
                        difficulty = get_pygame_input(screen, font, ["Simple heuristic", "Heurstic with positions", "Heuristic with chunks", "Tie avoidance"]) - 1
                    else:
                        difficulty = 0
                    players[i] = AIPlayer(algos[algo], difficulties[difficulty], statistics[algo], algoTypes[algo])

        while running and state.winner == 2:
            if GUI:
                if (len(state.boards) > 1):
                    for board in state.boards:
                        draw_bg(screen)
                        pieces = update_sprite(board, screen, ROWS, COLS)
                        pieces.update()
                        pieces.draw(screen)
                        players[not state.player].show_statistics(screen, font)
                        pygame.display.flip()
                        pygame_get_enter()
                draw_bg(screen)
                pieces = update_sprite(state.board, screen, ROWS, COLS)
                pieces.update()
                pieces.draw(screen)
                pygame.display.flip()
                state.boards = []
            if(not displayed):
                print("Turn:", "White" if state.player else "Black")        
                displayed = True
            if playerTypes[state.player] == 1:
                state = execute_player_move(screen, font, state, pieces)
            elif playerTypes[state.player] == 2:
                state = players[state.player].move(state)
                displayed = False
                if GUI:
                    players[not state.player].show_statistics(screen, font)
                    pygame_get_enter()
        announce_winner(state.winner,screen,font)
        first = False

if __name__=="__main__":
    main()