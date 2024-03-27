import pygame
white = 1
black = 0
space = 2
view = 3
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
        else:
            if self.isWhite == view:
                pygame.draw.circle(self.image, (11,255,102), (18, 18), 18)

    def drag(self, pos):
        self.rect.center = pos

    def place(self, pos,state, screen, font):    
        for piece in self.groups()[0]:
            if piece.rect.collidepoint(pos) and piece is not self :
                piece.placed = True
                self.placed = False
                piece.isWhite = self.isWhite
                self.isWhite = space
                self.image.fill((255, 255, 255, 0))
                self.rect.center = (128 + 48*self.x, 96 + 48*self.y)
                return state.move((self.y, self.x), (piece.y, piece.x), screen, font)
        self.rect.center = (128 + 48*self.x, 96 + 48*self.y)        
        return state.move((self.y, self.x), (self.y, self.x), screen, font)

def update_sprite(board ,screen, rows, cols,state = None):
    pieces = pygame.sprite.Group()

    for x in range(cols):
        for y in range(rows):
            if (board[y][x] == white):
                piece = Piece(white, x, y)
                pieces.add(piece)
            elif (board[y][x] == black): 
                piece = Piece(black, x, y)
                pieces.add(piece)
            elif((y,x) in state.available_moves):
                ##showing the moves for consecutive captures
                piece = Piece(view,x,y,False)
                pieces.add(piece)
            else:
                piece = Piece(space, x, y, False)
                pieces.add(piece)
    return pieces