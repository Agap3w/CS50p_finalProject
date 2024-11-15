#creating class SNAKE, movimento snake, screen_update

import pygame, sys, random
from pygame.math import Vector2 

class SNAKE: 
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(6,10), Vector2(7,10)] #3 vectors, one block each (remember x and y are # of block and not pixel here, as per following code structure)
        self.direction = Vector2(1,0)

    def draw_snake(self):
        for block in self.body:
            block_rect = pygame.Rect(block.x*cell_size, block.y*cell_size, cell_size, cell_size) #create a rect from the position
            pygame.draw.rect(screen, (200,200,200), block_rect) # draw a rect 

    # questa versione prevede il movimento di tutti i blocchi che scarrocciano nella posizione del blocco successivo (eliminando così l'ultimo), e creando un nuovo blocco (testa) nella direzioni in cui mi muovo.
    # secondo me posso efficientarla tenendo tutto il corpo fermo, muovendo la testa nella direzione e spostando la coda nella vecchia posizione della testa (ma non lo faccio qui)
    def move_snake(self):
        body_copy = self.body[0:-1] #copio tutto il vecchio corpo, tranne l'ultimo blocco (coda)
        body_copy.insert(0, body_copy[0]+self.direction) #aggiungo nuovo blocco (testa) ARG= index, value
        self.body = body_copy[:] # setto il nuovo corpo che ho creato (body_copy) come corpo principale (self.body) i [:] servono a creare una shallow copy e a non linkare per sempre le due liste

class FRUIT:
    def __init__(self):
        self.x = random.randint(0,cell_number-1)
        self.y = random.randint(0,cell_number-1)
        self.pos = Vector2(self.x, self.y)
    
    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x*cell_size, self.pos.y*cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, (100,100,100), fruit_rect) 
        

pygame.init()

cell_size = 40
cell_number = 20

screen = pygame.display.set_mode((cell_number*cell_size, cell_number*cell_size)) 
clock = pygame.time.Clock() 

fruit = FRUIT()
snake = SNAKE() #creating snake obj from SNAKE class

SCREEN_UPDATE = pygame.USEREVENT #creo un evento
pygame.time.set_timer(SCREEN_UPDATE, 150) # questo evento verrà creato ogni 150ms

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # quando si verifica questo evento (che ho settato passivo ogni 150ms), fai partire la fz move_snake    
        if event.type == SCREEN_UPDATE:
            snake.move_snake()
        if event.type == pygame.KEYDOWN: #se premo un qualsiasi tasto, sotto specifico casistiche
            if event.key == pygame.K_UP: # se premo freccia su
                snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN: # se premo freccia giù
                snake.direction = Vector2(0,1)
            if event.key == pygame.K_LEFT: # se premo freccia sx
                snake.direction = Vector2(-1,0)
            if event.key == pygame.K_RIGHT: # se premo freccia dx
                snake.direction = Vector2(1,0)

    screen.fill((0,100,100)) 
    fruit.draw_fruit() 
    snake.draw_snake() #draw snake through class function
    pygame.display.update()
    clock.tick(60)
