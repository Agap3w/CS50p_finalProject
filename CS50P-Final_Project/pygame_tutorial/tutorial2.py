import pygame #importo pygame
import sys

pygame.init() #inizializzo pygame

#setto dimensioni schermo (in pixel?)
SCREEN_WIDTH = 800 
SCREEN_HEIGHT = 600

#creo WINDOW game (posso anche mettere le dimensioni dello schermo direttamente qui dentro senza dichiarare le variabili prima)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
clock = pygame.time.Clock() #preparo oggetto clock con cui definirò poi FPS target

#creo il PERSONAGGIO
player = pygame.Rect((300,250,50,50))

#creo il LOOP (altrimeti la schermata appare e scompare)
while True:

    # imposto colore di base della window (così quando passa il personaggio non lascia poi scia)
    screen.fill((0,0,0))

    #renderizzo il personaggio
    pygame.draw.rect(screen, (255, 0, 0), player)

    #EVENT HANDLER (keybindings)
    key = pygame.key.get_pressed()
    
    #bindo la "wasd" sui movimento
    if key[pygame.K_a] == True:
        player.move_ip(-1, 0) # x, y in asse cartesiano
    elif key[pygame.K_d] == True:
        player.move_ip(1, 0) # x, y in asse cartesiano
    elif key[pygame.K_w] == True:
        player.move_ip(0, -1) # x, y in asse cartesiano
    elif key[pygame.K_s] == True:
        player.move_ip(0, 1) # x, y in asse cartesiano
        

    #EVENT HANDLER (in questo caso per terminare il loop quando chiudo la finestra)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() #questo chiude il pygame.init
            sys.exit() #ma alcuni pezzi di programma potrebbero ancora stare runnando, quindi faccio anche un sys.exit per sicurezza

    #questo servea a refreshare le info e quindi far visualizzare correttamente tutti gli elementi che renderizzo dentro la window, come ad es. il personaggio
    pygame.display.update()
    clock.tick(60) #setto fps target (=max)
        
pygame.quit()
