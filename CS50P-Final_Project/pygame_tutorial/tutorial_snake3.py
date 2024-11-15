#Adding class MAIN, snake mangia, fruit respawn

import pygame, sys, random
from pygame.math import Vector2 

class SNAKE: 
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(6,10), Vector2(7,10)]
        self.direction = Vector2(1,0)
        self.new_block = False #creo bool per quando mangia

    def draw_snake(self):
        for block in self.body:
            block_rect = pygame.Rect(block.x*cell_size, block.y*cell_size, cell_size, cell_size) 
            pygame.draw.rect(screen, (200,200,200), block_rect) 

    def move_snake(self):
        # se non ha appena mangiato, muovo normalmente
        if self.new_block == False:
            body_copy = self.body[0:-1]
            body_copy.insert(0, body_copy[0]+self.direction) 
            self.body = body_copy[:] 

        #se ha appena mangiato, non perdo la coda (=mi allungo di uno)
        else:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0]+self.direction) 
            self.body = body_copy[:] 
            self.new_block = False #chiudo la bool, altrimenti si allunga ogni volta che si muove

    def add_block(self):
        self.new_block = True

class FRUIT:
    def __init__(self):
        self.x = random.randint(0,cell_number-1)
        self.y = random.randint(0,cell_number-1)
        self.pos = Vector2(self.x, self.y)
    
    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x*cell_size, self.pos.y*cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, (100,100,100), fruit_rect) 

    #metodo per respawn (= a init)
    def randomize(self):
        self.x = random.randint(0,cell_number-1)
        self.y = random.randint(0,cell_number-1)
        self.pos = Vector2(self.x, self.y)
        
class MAIN:
    #con questa classe creo gli altri oggetti (così non devo farlo dopo nel codice)
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
    
    #stessa logica, prima chiamavo direttamente la fz snake movimento, ora lo faccio tramite main (e posso aggiungere a questo contenitore altre fz come: check collision)     
    def update(self):
        self.snake.move_snake() 
        self.check_collision()

    #stessa logica, qui disegno gli elementi (prima lo facevo singolarmente, ora ho accorpato su main)
    def draw_elements(self):
        self.fruit.draw_fruit() 
        self.snake.draw_snake() 

    # gestisco il mangiare la frutta
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]: #se posiz frutta == posiz testa snake
            #riposiziono la frutta
            self.fruit.randomize()
            #allungo il serpente di 1 block
            self.snake.add_block()




pygame.init()

cell_size = 40
cell_number = 20

screen = pygame.display.set_mode((cell_number*cell_size, cell_number*cell_size)) 
clock = pygame.time.Clock() 

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN() #qui prima creavo due oggetti (snake e fruit) ora ne creo uno solo che in automatico chiama gli altri

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
 
        if event.type == SCREEN_UPDATE:
            main_game.update() #prima chiamavo il movimento dello snake, ora chiamo la main function che a sua volta muove lo snake (ma fa anche altre cose)

        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_UP:
                main_game.snake.direction = Vector2(0,-1) # su questi 4 IF ho dovuto cambiare da "snake.direction" a "main_game.snake.direction", perché non esiste un oggetto snake se non dentro main ora (?)
            if event.key == pygame.K_DOWN: 
                main_game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_LEFT: 
                main_game.snake.direction = Vector2(-1,0)
            if event.key == pygame.K_RIGHT: 
                main_game.snake.direction = Vector2(1,0)

    screen.fill((0,100,100)) 
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
