import pygame
import chess

# Costanti GUI
DIMENSION = 8  # Dimensione scacchiera 8x8
SQUARE_SIZE = 80
WIDTH = HEIGHT = DIMENSION * SQUARE_SIZE
FPS = 30

# Colori scacchiera
LIGHT_COLOR = (240, 217, 181)
DARK_COLOR = (181, 136, 99)

# Simboli Unicode per i pezzi
UNICODE_PIECES = {
    'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙',
    'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟'
}

# Inizializza Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game - Unicode Edition")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 60)  # Font per i simboli Unicode

# Disegna la scacchiera
def draw_board(screen):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = LIGHT_COLOR if (row + col) % 2 == 0 else DARK_COLOR
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Disegna i pezzi sulla scacchiera usando simboli Unicode
def draw_pieces(screen, board):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_symbol = UNICODE_PIECES[piece.symbol()]
            col = chess.square_file(square)
            row = chess.square_rank(square)
            text = font.render(piece_symbol, True, (0, 0, 0))
            text_rect = text.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2, (7 - row) * SQUARE_SIZE + SQUARE_SIZE // 2))
            screen.blit(text, text_rect)

# Converti coordinate mouse in posizione sulla scacchiera
def get_square_under_mouse(pos):
    x, y = pos
    col = x // SQUARE_SIZE
    row = 7 - (y // SQUARE_SIZE)
    return chess.square(col, row)

# Main loop
def main():
    chess_board = chess.Board()
    running = True
    selected_square = None

    while running:
        draw_board(screen)
        draw_pieces(screen, chess_board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                clicked_square = get_square_under_mouse(mouse_pos)
    
                if selected_square is None:
                    # Seleziona il pezzo
                    if chess_board.piece_at(clicked_square):
                        selected_square = clicked_square
                else:
                    # Effettua la mossa
                    move = chess.Move(selected_square, clicked_square)
                    if move in chess_board.legal_moves:
                        chess_board.push(move)
                    selected_square = None

        # Aggiorna il display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
