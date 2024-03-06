# import the pygame module, so you can use it
import pygame
import numpy
import time
from Piece import *
import random
import functools 
from minimax import execute_minimax_move
from copy import deepcopy


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
        self.board = numpy.zeros((5,9))
        self.player = 1
        self.capture = no_capture
        self.last_dir = None
        self.capture_positions = []
        self.white_pieces = 22
        self.black_pieces = 22
        self.white_captured = 0
        self.black_captured = 0
        self.available_moves = [(2,4)]
        self.moved_pos = []
        self.winner = 2 #2 for no winner, 0 for black, 1 for white
        for y in range(9):
            for x in range(2):
                self.board[x][y] = black
        for y in range(4):
            if(y%2==0):
                self.board[2][y] = black
            else:
                self.board[2][y] = white
        for y in range(5, 9):
            if(y%2==0):
                self.board[2][y] = white
            else:
                self.board[2][y] = black
        
        for y in range(9):
            for x in range(3, 5):
                self.board[x][y] = white
        self.board[2][4] = space
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
        if (x < 0 or x >= ROWS or y < 0 or y >= COLS):
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
        temp_left = left
        temp_right = right
        temp_up = up
        temp_down = down
        temp_up_left = up_left
        temp_up_right = up_right
        temp_down_left = down_left
        temp_down_right = down_right
        temp_avalable_moves = list()
        eval_vec=(move[0]-player_pos[0],move[1]-player_pos[1])
        
        while(self.possible_move(move,vector_sum(move,temp_up)) and (not is_same_orientation(eval_vec,temp_up))):
            temp_avalable_moves.append(vector_sum(move,temp_up))
            temp_up = vector_sum(temp_up,up)
        while(self.possible_move(move,vector_sum(move,temp_down)) and (not is_same_orientation(eval_vec,temp_down))):
            temp_avalable_moves.append(vector_sum(move,temp_down))
            temp_down = vector_sum(temp_down,down)
        while(self.possible_move(move,vector_sum(move,temp_left)) and (not is_same_orientation(eval_vec,temp_left))):
            temp_avalable_moves.append(vector_sum(move,temp_left))
            temp_left = vector_sum(temp_left,left)
        while(self.possible_move(move,vector_sum(move,temp_right))and (not is_same_orientation(eval_vec,temp_right))):
            temp_avalable_moves.append(vector_sum(move,temp_right))
            temp_right = vector_sum(temp_right,right)
        while(self.possible_move(move,vector_sum(move,temp_up_left))and (not is_same_orientation(eval_vec,temp_up_left))):
            temp_avalable_moves.append(vector_sum(move,temp_up_left))
            temp_up_left = vector_sum(temp_up_left,up_left)
        while(self.possible_move(move,vector_sum(move,temp_up_right))and (not is_same_orientation(eval_vec,temp_up_right))):
            temp_avalable_moves.append(vector_sum(move,temp_up_right))
            temp_up_right = vector_sum(temp_up_right,up_right)
        while(self.possible_move(move,vector_sum(move,temp_down_left))and (not is_same_orientation(eval_vec,temp_down_left))):
            temp_avalable_moves.append(vector_sum(move,temp_down_left))
            temp_down_left = vector_sum(temp_down_left,down_left)
        while(self.possible_move(move,vector_sum(move,temp_down_right))and (not is_same_orientation(eval_vec,temp_down_right))):
            temp_avalable_moves.append(vector_sum(move,temp_down_right))
            temp_down_right = vector_sum(temp_down_right,down_right)
        print(temp_avalable_moves)
        print(previous_state.moved_pos)
        
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
            while(temp[0]>=0 and temp[0]<5 and temp[1]>=0 and temp[1]<9):
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
            while(temp[0]>=0 and temp[0]<5 and temp[1]>=0 and temp[1]<9):
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
                    print("No more moves")
                    state_copy.player = not self.player
                    state_copy.moved_pos = []
            else:
                if(state_copy.available_moves == []):
                    state_copy.board[xi][yi] = self.board[xi][yi]
                    state_copy.board[x][y] = space
                state_copy.move_pos = []
                state_copy.player = not self.player
                            
            
            state_copy.capture = no_capture
            return state_copy
           

        else:
            print("Invalid move")
            return -1
    
    def in_bounds(self, x, y):
        return not (x < 0 or x >= ROWS or y < 0 or y >= COLS)

    def try_moves(self, x, y, in_sequence=False):
        states = []
        if not in_sequence:
            self.last_dir = None
            self.capture_positions = [(x, y)]
        else:
            states.append(self)
        
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

                state_copy.capture_move((x, y), moved_pos)
                states.extend(state_copy.try_moves(moved_pos[0], moved_pos[1], True))
            if self.in_bounds(back_x, back_y) and self.board[back_x][back_y] == (not self.player):
                state_copy = deepcopy(self)
                state_copy.capture = capture_by_withdrawal
                state_copy.last_dir = dir
                state_copy.capture_positions.append(moved_pos)

                state_copy.capture_move((x, y), moved_pos)
                states.extend(state_copy.try_moves(moved_pos[0], moved_pos[1], True))

        return states

    def try_non_captures(self, x, y):
        states = []

        for dir in self.possible_moves_2(x, y):
            moved_pos = vector_sum((x, y), dir)
            if self.in_bounds(moved_pos[0], moved_pos[1]) and self.board[moved_pos[0], moved_pos[1]] != space:
                continue

            state_copy = deepcopy(self)
            state_copy.capture = no_capture
            state_copy.board[x][y] = space
            state_copy.board[moved_pos[0]][moved_pos[1]] = self.player
            states.append(state_copy)
        
        return states



    def get_available_captures(self):
        states = []
        for x in range(ROWS):
            for y in range(COLS):
                if self.board[x][y] == self.player:
                    states.extend(self.try_moves(x, y))

        return states
    
    def get_available_non_captures(self):
        states = []
        for x in range(ROWS):
            for y in range(COLS):
                if self.board[x][y] == self.player:
                    states.extend(self.try_non_captures(x, y))

        return states
    
    def get_all_moves(self):
        moves = self.get_available_captures()
        if len(moves) == 0:
            moves = self.get_available_non_captures()
        return moves

    def check_win(self):
        if self.white_pieces == 0:
            self.winner = black
        elif self.black_pieces == 0:
            self.winner = white
        else:
            self.winner = 2
        return self.winner

        


        
 
def draw_motif(screen, x, y, size):
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y, size, size), width=1)
    pygame.draw.line(screen, (0, 0, 0), (x+size/2, y), (x+size/2, y+size))
    pygame.draw.line(screen, (0, 0, 0), (x, y+size/2), (x+size, y+size/2))
    pygame.draw.line(screen, (0, 0, 0), (x, y), (x+size, y+size))
    pygame.draw.line(screen, (0, 0, 0), (x, y+size), (x+size, y))

def draw_bg(screen):
    screen.fill((255, 255, 255))
    for x in range(4):
        for y in range(2):
            draw_motif(screen, 128 + 96*x, 96*(y+1), 96)

def get_pygame_input(screen, font, opts):
    opts = list(map(lambda num, opt: f"{num}: {opt}", range(1, len(opts)+1), opts))
    for i in range(len(opts)):
        display_text = font.render(opts[len(opts)-i-1], True, (0,0,0))
        textRect = display_text.get_rect()
        textRect.bottomleft = (0, 480-24*i)
        screen.blit(display_text, textRect)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                if key >= '1' and key <= str(len(opts)):
                    rect = pygame.rect.Rect(0, 480-24*(len(opts)-1), 640, 24*(len(opts)-1))
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
                pieces = update_sprite(state,screen)
                dragging = None
                return state, pieces
            if event.type == pygame.MOUSEMOTION and dragging:
                dragging.drag(pygame.mouse.get_pos())

def execute_random_move(screen, font, state, pieces):
    moves = state.get_all_moves()
    move = random.choice(moves)
    move.player = not move.player
    pieces = update_sprite(move,screen)
    return move, pieces

# define a main function
def main():
     
    state = State()
    #test = state.get_all_moves()

    pygame.init()
    pygame.display.set_caption("Fanorona")
    font = pygame.font.Font(pygame.font.get_default_font(), 24)
     
    # create a surface on screen that has the size of 640 x 480
    screen = pygame.display.set_mode((640,480))
    #game = State()

    running = True
    pieces=update_sprite(state,screen)
    global displayed
    draw_bg(screen)
    pieces.update()
    pieces.draw(screen)
    pygame.display.flip()
    mode=get_pygame_input(screen, font, ["Human vs Human", "Human vs AI", "AI vs AI"])
    players = None
    if mode == 1:
        players = (1, 1)
    elif mode == 2:
        players = (2, 1)
    elif mode == 3:
        players = (2, 2)
    while running and state.winner == 2:
        if(not displayed):
            print("Turn:", "White" if state.player else "Black")        
            displayed = True
        if players[state.player] == 1:
            state, pieces = execute_player_move(screen, font, state, pieces)
        elif players[state.player] == 2:
            state, pieces = execute_minimax_move(screen, font, state, pieces)

if __name__=="__main__":
    main()