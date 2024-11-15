import pygame, sys

pygame.init()
screen = pygame.display.set_mode((400, 500)) 
clock = pygame.time.Clock() 

test_surface = pygame.Surface((100,200)) #anche qui come argomento una tuple (w,h)
test_surface.fill((30,30,31)) # cambio il colore dell'elemento
x_pos=200 #setting a variable that i will use for the position of the element

test_rect = pygame.Rect((100,200,100,100)) # creo rettangolo, arg è tuple (x,y,w,h)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((0,100,100)) # cambio il colore del canvas
    pygame.draw.rect(screen, (200,200,200), test_rect) #fz per disegnare rettangolo con (surface di sfondo, color, variabile). E' customizzabile (es se al posto di .rect metto .ellipse mi disegna un cerchio)
    screen.blit(test_surface, (x_pos,250)) #BlIT= Block Image Transfer, tuple con posizione cartesiana (x,y) partendo da top-left corner
    x_pos+=1
    pygame.display.update()
    clock.tick(60)
