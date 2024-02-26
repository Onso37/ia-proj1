# import the pygame module, so you can use it
import pygame

white = True
black = False


class Piece(pygame.sprite.Sprite):

    def __init__(self, isWhite, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((36, 36), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        if(isWhite):
            pygame.draw.circle(self.image, (255, 255, 255), (18, 18), 18)
            pygame.draw.circle(self.image, (0,0,0), (18, 18), 18, width=2)
        else:
            pygame.draw.circle(self.image, (0,0,0), (18, 18), 18)
        
        self.x = x
        self.y = y
        self.rect.center = (128 + 48*x, 96 + 48*y)

    def update(self, pos):
        if self.rect.collidepoint(pos):
            self.clicked()

    def clicked(self):
        print(f"Piece ({self.x},{self.y}) was clicked!")

def draw_motif(screen, x, y, size):
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y, size, size), width=1)
    pygame.draw.line(screen, (0, 0, 0), (x+size/2, y), (x+size/2, y+size))
    pygame.draw.line(screen, (0, 0, 0), (x, y+size/2), (x+size, y+size/2))
    pygame.draw.line(screen, (0, 0, 0), (x, y), (x+size, y+size))
    pygame.draw.line(screen, (0, 0, 0), (x, y+size), (x+size, y))

# define a main function
def main():
     
    pygame.init()
    pygame.display.set_caption("Fanorona")
     
    # create a surface on screen that has the size of 640 x 480
    screen = pygame.display.set_mode((640,480))
    pieces = pygame.sprite.Group()
     
    running = True
     
    screen.fill((255, 255, 255))
    for x in range(4):
        for y in range(2):
            draw_motif(screen, 128 + 96*x, 96*(y+1), 96)
    
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

    pieces.update((0, 0))
    pieces.draw(screen)

    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                pieces.update(pygame.mouse.get_pos())
     
if __name__=="__main__":
    main()