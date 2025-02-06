import pygame
import chess

# Imposta dimensioni finestra
DIMENSION = 8  # Dimensioni della scacchiera (8x8)
SQUARE_SIZE = 80  # Dimensione dei quadrati
WIDTH = HEIGHT = DIMENSION * SQUARE_SIZE
FPS = 30

# Colori
LIGHT_COLOR = (240, 217, 181)
DARK_COLOR = (181, 136, 99)

# Inizializza Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Carica immagini dei pezzi
piece_images = {}
def load_images():
    pieces = ['r', 'n', 'b', 'q', 'k', 'p', 'R', 'N', 'B', 'Q', 'K', 'P']
    for piece in pieces:
        piece_images[piece] = pygame.transform.scale(
            pygame.image.load(f"images/{piece}.png"), 
            (SQUARE_SIZE, SQUARE_SIZE)
        )

# Disegna la scacchiera
def draw_board(screen):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = LIGHT_COLOR if (row + col) % 2 == 0 else DARK_COLOR
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Disegna i pezzi sulla scacchiera
def draw_pieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board.piece_at(row * 8 + col)
            if piece:
                piece_symbol = piece.symbol()
                screen.blit(piece_images[piece_symbol], pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Main loop
def main():
    chess_board = chess.Board()
    load_images()
    running = True

    while running:
        draw_board(screen)
        draw_pieces(screen, chess_board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Aggiorna il display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
