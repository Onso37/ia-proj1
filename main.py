# import the pygame module, so you can use it
import pygame
import numpy
from copy import deepcopy


capture_by_approach=0
capture_by_withdrawal=1
no_capture=-1

white = 1
black = 0
space = 2
player_turn = white  #white starts
left = (0,-1)
right = (0, 1)
up = (-1,0)
down = (1,0)
up_left = (-1,-1)
up_right =(-1,1)
down_left = (1,-1)
down_right = (1,1)
displayed = False

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

class State:
    def __init__(self):
        self.board = numpy.zeros((5,9))
        self.player = 1
        self.capture = no_capture
        self.white_pieces = 22
        self.black_pieces = 22
        self.white_captured = 0
        self.black_captured = 0
        self.available_moves = [(2,4)]
        self.winner = -1 #-1 for no winner, 0 for black, 1 for white
        for y in range(9):
            for x in range(2):
                self.board[x][y] = black
        for y in range(9):
            if(y != 4):
                if(y%2==0):
                    self.board[2][y] = black
                else:
                    self.board[2][y] = white
        
        for y in range(9):
            for x in range(3, 5):
                self.board[x][y] = white
        self.board[2][4] = space

    def possible_move(self,player_pos,move):
        xi,yi=player_pos
        x,y = move
        if(self.player != self.board[xi][yi] ): 
            return False;
        if(is_diagonal(xi,yi,x,y)):
            if((is_even(xi) and is_even(yi)) or (not is_even(xi) and not is_even(yi))):
                if(self.board[x][y] == space):
                    return True
        else:
            if(self.board[x][y] == space):
                return True

        return False
    
    def possible_moves(self,player_pos):
        temp_left = left
        temp_right = right
        temp_up = up
        temp_down = down
        temp_up_left = up_left
        temp_up_right = up_right
        temp_down_left = down_left
        temp_down_right = down_right
        temp_avalable_moves = list()
        while(self.possible_move(player_pos,vector_sum(player_pos,temp_up))):
            temp_avalable_moves.append(vector_sum(player_pos,temp_up))
            temp_up = vector_sum(temp_up,up)
        while(self.possible_move(player_pos,vector_sum(player_pos,temp_down))):
            temp_avalable_moves.append(vector_sum(player_pos,temp_down))
            temp_down = vector_sum(temp_down,down)
        while(self.possible_move(player_pos,vector_sum(player_pos,temp_left))):
            temp_avalable_moves.append(vector_sum(player_pos,temp_left))
            temp_left = vector_sum(temp_left,left)
        while(self.possible_move(player_pos,vector_sum(player_pos,temp_right))):
            temp_avalable_moves.append(vector_sum(player_pos,temp_right))
            temp_right = vector_sum(temp_right,right)
        while(self.possible_move(player_pos,vector_sum(player_pos,temp_up_left))):
            temp_avalable_moves.append(vector_sum(player_pos,temp_up_left))
            temp_up_left = vector_sum(temp_up_left,up_left)
        while(self.possible_move(player_pos,vector_sum(player_pos,temp_up_right))):
            temp_avalable_moves.append(vector_sum(player_pos,temp_up_right))
            temp_up_right = vector_sum(temp_up_right,up_right)
        while(self.possible_move(player_pos,vector_sum(player_pos,temp_down_left))):
            temp_avalable_moves.append(vector_sum(player_pos,temp_down_left))
            temp_down_left = vector_sum(temp_down_left,down_left)
        while(self.possible_move(player_pos,vector_sum(player_pos,temp_down_right))):
            temp_avalable_moves.append(vector_sum(player_pos,temp_down_right))
            temp_down_right = vector_sum(temp_down_right,down_right)
       
        return temp_avalable_moves
    
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
        return self.board
      
    def move(self,player_pos,move):
        xi,yi=player_pos
        x,y = move
        state_copy = deepcopy(self)
        if(move in self.available_moves):
            state_copy.capture_move(player_pos,move)
            state_copy.board[x][y] = state_copy.board[xi][yi]
            state_copy.board[xi][yi] = space
            state_copy.available_moves = state_copy.possible_moves(move)
            state_copy.player = not state_copy.player            
            return state_copy
        else:
            print("Invalid move")
            return -1

        
class Piece(pygame.sprite.Sprite):
    
    def __init__(self, isWhite, x, y, placed=True):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((36, 36), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.isWhite = isWhite
        self.placed = placed

        self.x = x
        self.y = y
        self.rect.center = (128 + 48*x, 96 + 48*y)

    def update(self):
        if self.placed:
            if self.isWhite:
                pygame.draw.circle(self.image, (255, 255, 255), (18, 18), 18)
                pygame.draw.circle(self.image, (0,0,0), (18, 18), 18, width=2)
            else:
                pygame.draw.circle(self.image, (0,0,0), (18, 18), 18)

    def drag(self, pos):
        self.rect.center = pos

    def place(self, pos):        
        for piece in self.groups()[0]:
            if piece.rect.collidepoint(pos) and piece is not self :
                piece.placed = True
                self.placed = False
                piece.isWhite = self.isWhite
                self.isWhite = space
                self.image.fill((255, 255, 255, 0))
                self.rect.center = (128 + 48*self.x, 96 + 48*self.y)
                return
        
        self.rect.center = (128 + 48*self.x, 96 + 48*self.y)
   
        
 
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

# define a main function
def main():
     
    pygame.init()
    pygame.display.set_caption("Fanorona")
     
    # create a surface on screen that has the size of 640 x 480
    screen = pygame.display.set_mode((640,480))
    pieces = pygame.sprite.Group()
     
    running = True
    dragging = None
    
    for x in range(9):
        for y in range(2):
            piece = Piece(black, x, y)
            pieces.add(piece)
    for x in range(9):
        if(x != 4):
            if(x%2==0):
                piece = Piece(black, x, 2)
                pieces.add(piece)
            else:
                piece = Piece(white, x, 2)
                pieces.add(piece)
       
    for x in range(9):
        for y in range(3, 5):
            piece = Piece(white, x, y)
            pieces.add(piece)

    center_piece = Piece(space, 4, 2, False)
    pieces.add(center_piece)

    while running:
        draw_bg(screen)
        pieces.update()
        pieces.draw(screen)
        pygame.display.flip()
        global displayed

        if(player_turn == white and not displayed):
            print("White's turn")
            displayed = True
        elif(player_turn == black and not displayed):
            print("Black's turn")
            displayed = True
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not dragging:
                for piece in pieces:
                    if piece.rect.collidepoint(pygame.mouse.get_pos()):
                        dragging = piece
                        piece.dragging = True
            if event.type == pygame.MOUSEBUTTONUP and dragging:
                dragging.place(pygame.mouse.get_pos())
                dragging = None
            if event.type == pygame.MOUSEMOTION and dragging:
                dragging.drag(pygame.mouse.get_pos())

if __name__=="__main__":
    main()