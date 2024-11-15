#gestisco il game over (contro muro o contro se stesso)

import pygame, sys, random
from pygame.math import Vector2 

class SNAKE: 
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)] #modificato il valore dei vettori per rendere la testa la X più alta (=la più a dx) coerentemente con la default direction della riga successiva, ovvero verso dx 
        self.direction = Vector2(1,0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            block_rect = pygame.Rect(block.x*cell_size, block.y*cell_size, cell_size, cell_size) 
            pygame.draw.rect(screen, (200,200,200), block_rect) 

    def move_snake(self):
        if self.new_block == False:
            body_copy = self.body[0:-1]
            body_copy.insert(0, body_copy[0]+self.direction) 
            self.body = body_copy[:] 

        else:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0]+self.direction) 
            self.body = body_copy[:] 
            self.new_block = False

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

    def randomize(self):
        self.x = random.randint(0,cell_number-1)
        self.y = random.randint(0,cell_number-1)
        self.pos = Vector2(self.x, self.y)
        
class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
    
    def update(self):
        self.snake.move_snake() 
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.fruit.draw_fruit() 
        self.snake.draw_snake() 

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]: 
            self.fruit.randomize()
            self.snake.add_block()

    def check_fail(self):
        #check if snake head outside screen
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        
        #check if snake head hit snake body
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()


    #definying game over
    def game_over(self):
        pygame.quit()
        sys.exit(1)

pygame.init()

cell_size = 40
cell_number = 20

screen = pygame.display.set_mode((cell_number*cell_size, cell_number*cell_size)) 
clock = pygame.time.Clock() 

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
 
        if event.type == SCREEN_UPDATE:
            main_game.update()

        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_UP and main_game.snake.direction.y != 1: #aggiungo la seconda condizione (and..) per evitare inversioni di 180° !!-NB-!! Se premo due pulsanti insieme o molto velocemente, riesco ancora a "suicidarmi" su me stesso, da risolvere !!-NB-!!
                main_game.snake.direction = Vector2(0,-1) 
            if event.key == pygame.K_DOWN and main_game.snake.direction.y != -1: #aggiungo la seconda condizione
                main_game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_LEFT and main_game.snake.direction.x != 1: #aggiungo la seconda condizione
                main_game.snake.direction = Vector2(-1,0)
            if event.key == pygame.K_RIGHT and main_game.snake.direction.x != -1: #aggiungo la seconda condizione
                main_game.snake.direction = Vector2(1,0)

    screen.fill((0,100,100)) 
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
