#creo e aggiungo le grafiche (fruit - snake - background)

import pygame, sys, random
from pygame.math import Vector2 

class SNAKE: 
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)] 
        self.direction = Vector2(1,0)
        self.new_block = False

        #tutto questo spataffione di 14 elementi serve a caricare le immagini che ci servono per customizzare le varianti del serpente in base al movimento
        self.head_up = pygame.image.load('../static/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('../static/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('../static/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('../static/head_left.png').convert_alpha()
		
        self.tail_up = pygame.image.load('../static/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('../static/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('../static/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('../static/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('../static/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('../static/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('../static/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('../static/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('../static/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('../static/body_bl.png').convert_alpha()

    def draw_snake(self):

        self.update_head_graphics() #aggiungo questa per poter scegliere di volta in volta la grafica giusta (tra le 14 di cui sopra) da applicare alla testa
        self.update_tail_graphics() #stessa cosa, per la coda

        for index,block in enumerate(self.body):
            block_rect = pygame.Rect(block.x*cell_size, block.y*cell_size, cell_size, cell_size) # still need a rect for the position 

            # draw custom graphics (here for head) 
            if index == 0:
                screen.blit(self.head, block_rect)

            # tail     
            elif index == len(self.body)-1:
                screen.blit(self.tail, block_rect) 

            #rest of the body    
            else:
                previous_block = self.body[index +1] - block #posiz relativa tra i due blocchi
                following_block= self.body[index-1] - block #same 
                
                # se prev e follow block hanno stessa x, vuol dire che sono verticalmente allineati (aka i due blocchi hanno la stessa direzione verticale) e posso mandare rendering del corpo verticale
                if previous_block.x == following_block.x:
                    screen.blit(self.body_vertical, block_rect)

                # se prev e follow block hanno stessa y, vuol dire che sono orizzontalmente allineati e posso mandare rendering del corpo orizzontale
                if previous_block.y == following_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                
                #gestisco le 4 curvature del corpo (codificate in base agli angoli, es tr = topright)
                else:
                    if previous_block.x ==  -1 and following_block.y== -1 or previous_block.y ==  -1 and following_block.x== -1:
                        screen.blit(self.body_tl, block_rect)
                    if previous_block.x ==  1 and following_block.y== 1 or previous_block.y ==  1 and following_block.x== 1:
                        screen.blit(self.body_br, block_rect)
                    if previous_block.x ==  -1 and following_block.y== 1 or previous_block.y ==  1 and following_block.x== -1:
                        screen.blit(self.body_bl, block_rect)
                    if previous_block.x ==  1 and following_block.y== -1 or previous_block.y ==  -1 and following_block.x== 1:
                        screen.blit(self.body_tr, block_rect)

    def update_head_graphics(self):

        head_relation = self.body[1] - self.body[0] #sottraendo i due blocchi ottengo la loro posizione relativa, in questo caso quindi la "direzione" della testa
        
        #gestisco le casistiche delle diverse direzioni (= diverse grafiche per la testa)
        if head_relation == Vector2(1,0): self.head = self.head_left # caso in cui la testa è a sx del 2nd blocco, quindi direzione: <-- 
        elif head_relation == Vector2(-1,0): self.head = self.head_right # caso in cui la testa è a dx del 2nd blocco, quindi direzione: --> 
        elif head_relation == Vector2(0,1): self.head = self.head_up # caso in cui la testa è sopra il 2nd blocco, quindi direzione: ^ 
        elif head_relation == Vector2(0,-1): self.head = self.head_down  # caso in cui la testa è sotto il 2nd blocco, quindi direzione: v 

    def update_tail_graphics(self):

        tail_relation = self.body[-2] - self.body[-1] #sottraendo i due blocchi ottengo la loro posizione relativa, in questo caso quindi la "direzione" della testa
        
        #gestisco le casistiche delle diverse direzioni (= diverse grafiche per la testa)
        if tail_relation == Vector2(1,0): self.tail = self.tail_left # caso in cui la testa è a sx del 2nd blocco, quindi direzione: <-- 
        elif tail_relation == Vector2(-1,0): self.tail = self.tail_right # caso in cui la testa è a dx del 2nd blocco, quindi direzione: --> 
        elif tail_relation == Vector2(0,1): self.tail = self.tail_up # caso in cui la testa è sopra il 2nd blocco, quindi direzione: ^ 
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_down  # caso in cui la testa è sotto il 2nd blocco, quindi direzione: v 


















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
        scaled_legna = pygame.transform.scale(legna, (cell_size, cell_size)) # Resize the image to fit the rectangle size
        screen.blit(scaled_legna, fruit_rect)
        #pygame.draw.rect(screen, (100,100,100), fruit_rect) 

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
        self.draw_grass()
        self.fruit.draw_fruit() 
        self.snake.draw_snake() 

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]: 
            self.fruit.randomize()
            self.snake.add_block()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit(1)

    #creo background a scacchi
    def draw_grass(self):
        
        grass_colour = (10,110,110) #setto colore

        #per ogni riga pari...
        for row in range(cell_number):
            if row % 2 == 0:
                #...disegna ogni colonna pari
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size) #x,y,w,h
                        pygame.draw.rect(screen, grass_colour, grass_rect)
            # per ogni riga dispari invece...                    
            else:
                # disegna ogni colonna dispari
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size) #x,y,w,h
                        pygame.draw.rect(screen, grass_colour, grass_rect)

pygame.init()

cell_size = 40
cell_number = 20

screen = pygame.display.set_mode((cell_number*cell_size, cell_number*cell_size)) 
clock = pygame.time.Clock()
legna = pygame.image.load("../static/legna.png").convert_alpha() #con la prima fz carico l'immagine nel programma, con la seconda la converto in un altro formato (non png o bmp, bensì alfa) più leggero con cui py lavora meglio

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
            if event.key == pygame.K_UP and main_game.snake.direction.y != 1: 
                main_game.snake.direction = Vector2(0,-1) 
            if event.key == pygame.K_DOWN and main_game.snake.direction.y != -1: 
                main_game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_LEFT and main_game.snake.direction.x != 1: 
                main_game.snake.direction = Vector2(-1,0)
            if event.key == pygame.K_RIGHT and main_game.snake.direction.x != -1: 
                main_game.snake.direction = Vector2(1,0)

    screen.fill((0,100,100)) 
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
