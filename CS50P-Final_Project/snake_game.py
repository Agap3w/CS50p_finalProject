import pygame, sys, random
from pygame.math import Vector2 

#il serpente
class SNAKE: 
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)] 
        self.direction = Vector2(0,0)
        self.new_block = False

        self.head_up = pygame.image.load('static/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('static/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('static/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('static/head_left.png').convert_alpha()
		
        self.tail_up = pygame.image.load('static/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('static/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('static/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('static/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('static/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('static/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('static/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('static/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('static/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('static/body_bl.png').convert_alpha()

        self.crunch_sound = pygame.mixer.Sound("static/crunch.wav") #uploado un sound

    def draw_snake(self):

        self.update_head_graphics()
        self.update_tail_graphics() 

        for index,block in enumerate(self.body):
            block_rect = pygame.Rect(block.x*cell_size, block.y*cell_size, cell_size, cell_size) 

            if index == 0:
                screen.blit(self.head, block_rect)
   
            elif index == len(self.body)-1:
                screen.blit(self.tail, block_rect) 
  
            else:
                previous_block = self.body[index +1] - block 
                following_block= self.body[index-1] - block 
                
                if previous_block.x == following_block.x:
                    screen.blit(self.body_vertical, block_rect)

                if previous_block.y == following_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                
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

        head_relation = self.body[1] - self.body[0] 
        
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right 
        elif head_relation == Vector2(0,1): self.head = self.head_up 
        elif head_relation == Vector2(0,-1): self.head = self.head_down 

    def update_tail_graphics(self):

        tail_relation = self.body[-2] - self.body[-1] 
        
        if tail_relation == Vector2(1,0): self.tail = self.tail_left 
        elif tail_relation == Vector2(-1,0): self.tail = self.tail_right 
        elif tail_relation == Vector2(0,1): self.tail = self.tail_up 
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_down

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

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(0,0)

#la frutta
class FRUIT:
    def __init__(self):
        self.x = random.randint(0,cell_number-1)
        self.y = random.randint(0,cell_number-1)
        self.pos = Vector2(self.x, self.y)
    
    
    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x*cell_size, self.pos.y*cell_size, cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0,cell_number-1)
        self.y = random.randint(0,cell_number-1)
        self.pos = Vector2(self.x, self.y)

#MAIN (include serpente + frutta + background + dinamiche di gioco come collisione e game_over)        
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
        self.draw_score() 

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]: 
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()
        
        #se frutta respawna su serpente, ripeto respawn
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()

    def draw_grass(self):
        
        grass_colour = (135,170,60)

        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_colour, grass_rect)       
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size) 
                        pygame.draw.rect(screen, grass_colour, grass_rect)

    # creo e disegno score (il font l'ho creato sotto invece, fuori dalle classi)
    def draw_score(self):
        score_text = str(len(self.snake.body) - 3) # converto int in str perché è più semplice poi da printare/gestire (boh!)
        score_surface = game_font.render(score_text,True,(0,0,0)) #arg = (text, bool:anti-alias, color)
        
        # creo variabili che mi servono per il blit poi
        score_x = cell_size * cell_number - 60
        score_y = cell_size * cell_number - 40
        score_rect = score_surface.get_rect(center = (score_x, score_y)) # creo il rettangolo dalla score_surface
        apple_rect = apple.get_rect(midright = (score_rect.left-10, score_rect.centery)) # creo il rettangolo dalla apple(surface). midright mi permette di piazzarmi direttamente sul rettangolo adiacente
        score_frame_rect = pygame.Rect(apple_rect.left, apple_rect.top,cell_size+score_rect.width+20, cell_size)

        #posiziono i quattro elementi che compongono lo score:
        pygame.draw.rect(screen, (167,209,61), score_frame_rect) # il rettangolino di sfondo
        screen.blit(score_surface, score_rect) # il numero
        screen.blit(apple, apple_rect) # la mela
        pygame.draw.rect(screen, (110,110,110), score_frame_rect, 2) # la cornice



pygame.init()

cell_size = 40
cell_number = 20

screen = pygame.display.set_mode((cell_number*cell_size, cell_number*cell_size)) 
clock = pygame.time.Clock()
apple = pygame.image.load("static/apple.png").convert_alpha()
game_font = pygame.font.Font(None, 25) #ARG = (font, fontsize). Come font posso usare 'None' oppure uploadare un '../static/font.ttf'

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

    screen.fill((145,182,63)) 
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)