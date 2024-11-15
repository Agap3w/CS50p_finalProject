import pygame, sys

pygame.init()
screen = pygame.display.set_mode((400, 500)) 
clock = pygame.time.Clock() 

test_surface = pygame.Surface((100,200))
test_surface.fill((30,30,31)) 

test_rect = test_surface.get_rect(center = (200,250)) # così creo invece il rettangolo partendo dalla surface, e posso specificare nelle parentesi la posizione in cui metterlo

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((0,100,100)) 
    screen.blit(test_surface, test_rect) # in questo modo posso usare la variabile rect ANCHE come posizione cardinale 
    test_rect.right +=1 # in questo modo muovo il rettangolo sull'asse orizzontale di 1px su x alla volta (poco importa se scrivo .right o .left, la direzione la da il numero)
    pygame.display.update()
    clock.tick(60)
