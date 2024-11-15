#creo class FRUIT, griglia

import pygame, sys, random
from pygame.math import Vector2 

#creo classe player (fruit in questo caso)
class FRUIT:
    def __init__(self):
        #create X and Y position
        self.x = random.randint(0,cell_number-1)
        self.y = random.randint(0,cell_number-1)
        #creo un vector con le due variabili appena dichiarate
        self.pos = Vector2(self.x, self.y)
    
    def draw_fruit(self):
        #create a rect
        fruit_rect = pygame.Rect(self.pos.x*cell_size, self.pos.y*cell_size, cell_size, cell_size) #x,y,w,h
        #draw the rect
        pygame.draw.rect(screen, (100,100,100), fruit_rect) #surface, color, rect
        

pygame.init()

#creo una specie di griglia per definire le dimensioni del display
cell_size = 40
cell_number = 20

screen = pygame.display.set_mode((cell_number*cell_size, cell_number*cell_size)) # passo da pixel fissi a variabili (la grid che ho creato prima che sarà = 800x800) 
clock = pygame.time.Clock() 

#creo l'oggetto dalla classe 
fruit = FRUIT()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0,100,100)) 
    fruit.draw_fruit() #con questo comando mostro sullo schermo l'oggetto fruit che ho creato
    pygame.display.update()
    clock.tick(60)
