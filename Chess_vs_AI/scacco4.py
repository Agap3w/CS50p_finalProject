# TO DO:
# refactoring in masterclass ChessGame + subclass GUI, SoundManager, GameLogic
# aggiungo GUI:
# 1. schermata introduttiva
# 2. promo choice
# 3. game over 

# MINOR:
# aggiungere pulsante per arrendersi / chiedere la patta

# VERY MINOR:
# customizzo grafica pezzi
# Move Highlighting: Show legal moves for the selected piece NB attivo solo dopo mossa irregolare
# Piece Capturing Animation (Optional): Provide visual feedback for captures. gIdea= barra nera laterale in cui scorrono dal basso verso l'alto gli "spiriti" dei pezzi, con le ali che flappano e un breve bubble text tipo "was I a good {piece}" 

# DOUBT:
# sql

import pygame
import chess

# GUI Constants
DIMENSION = 8
SQUARE_SIZE = 80
WIDTH = HEIGHT = DIMENSION * SQUARE_SIZE
FPS = 30

# Board colors
LIGHT_COLOR = (240, 217, 181)
DARK_COLOR = (181, 136, 99)

# Dict con key = pychess piece.symbol() e value = disegno Unicode
UNICODE_PIECES = {
    'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙',
    'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟'
}

def init_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess vs AI")
    # scelgo un font che supporta Unicode chess symbols
    try:
        font = pygame.font.SysFont('segoe ui symbol', 60)  # Windows
    except:
        try:
            font = pygame.font.SysFont('arial unicode ms', 60)  # Alternativa
        except:
            font = pygame.font.Font(None, 60)  # Fallback
    return screen, font

#disegno la scacchiera
def draw_board(screen):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = LIGHT_COLOR if (row + col) % 2 == 0 else DARK_COLOR
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

#evidenzia square selezionata
def draw_selected_square(screen, square):
    if square is not None: # se è selezionata
        col = chess.square_file(square)
        row = chess.square_rank(square)
        pygame.draw.rect(screen, (255, 255, 0, 50), 
                        pygame.Rect(col * SQUARE_SIZE, (7 - row) * SQUARE_SIZE, 
                                  SQUARE_SIZE, SQUARE_SIZE), 3)

#disegno i pezzi sfruttando pychess
def draw_pieces(screen, board, font):
    for square in chess.SQUARES:
        piece = board.piece_at(square) # prende il pezzo sulla square corrispondente
        if piece: # se esiste   
            piece_symbol = UNICODE_PIECES[piece.symbol()] # prende il disegno corretto
            col = chess.square_file(square) #prende num colonna (prima avevo un 0-64)
            row = chess.square_rank(square) #prende num riga
            #aggiungo colore e mando a schermo (rect+blit)
            color = (255, 255, 255) if piece.color else (0, 0, 0)
            text = font.render(piece_symbol, True, color)
            text_rect = text.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2, 
                                            (7 - row) * SQUARE_SIZE + SQUARE_SIZE // 2))
            screen.blit(text, text_rect)

#check per GameOver (incluso Stallo)
def check_game_over(chess_board):
    if chess_board.is_checkmate():
        print("Checkmate!")
        return True
    elif chess_board.is_stalemate() or chess_board.is_insufficient_material():
        print("Draw!")
        return True
    return False

#converte posizione del mouse in square (per localizzare click?)
def get_square_under_mouse(pos):
    x, y = pos
    col = x // SQUARE_SIZE
    row = 7 - (y // SQUARE_SIZE)
    return chess.square(col, row)

#gestisco promozione (per ora sempre in Queen)
def handle_pawn_promotion(chess_board, selected_square, clicked_square, move):
    if chess_board.piece_at(selected_square).piece_type == chess.PAWN:
        if (chess_board.turn == chess.WHITE and chess.square_rank(clicked_square) == 7) or \
           (chess_board.turn == chess.BLACK and chess.square_rank(clicked_square) == 0):
            move.promotion = chess.QUEEN
    return move 

#gestisco la logica da click a mossa (ed ev. pawn promotion)
def handle_move(chess_board, selected_square, clicked_square, sound_manager):
    #se non ho ancora selezionato niente..  
    if selected_square is None:
        piece = chess_board.piece_at(clicked_square)
        # ..allora registro solo se il click è su un mio pezzo + nel mio turno
        if piece and piece.color == chess_board.turn:
            return clicked_square
    
    else: #se invece ho già un pezzo selezionato
        move = chess.Move(selected_square, clicked_square)
        move = handle_pawn_promotion(chess_board, selected_square, clicked_square, move)

        # Check se mossa consentita > pusho e suono
        if move in chess_board.legal_moves:
            captured_piece = chess_board.piece_at(clicked_square)  # Piece that was captured, if any 
            chess_board.push(move)
            sound_manager.play_move_sounds(move, captured_piece, chess_board.is_check())

        return None

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.load_sounds()

    def load_sounds(self):
        sound_files = {
            "move": "static/move.wav",
            "gnam": "static/gnam.wav",
            "check": "static/check.wav",
            "promo": "static/promo.wav"
        }
        
        for sound_name, file_path in sound_files.items():
            try:
                self.sounds[sound_name] = pygame.mixer.Sound(file_path)
            except pygame.error as e:
                print(f"Warning: Could not load sound {sound_name} from {file_path}: {e}")
                self.sounds[sound_name] = None
                
        # Set volumes only for successfully loaded sounds
        for sound_name, volume in [("move", 0.4), ("gnam", 1.0), ("promo", 1.2), ("check", 1.2)]:
            if self.sounds[sound_name]:
                self.sounds[sound_name].set_volume(volume)
            
    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()

    def play_move_sounds(self, move, captured_piece, is_check):
        self.play_sound("move")
        if move.promotion:
            self.play_sound("promo")
        if captured_piece:
            self.play_sound("gnam")
        if is_check:
            self.play_sound("check")

def main():
    screen, font = init_game()
    chess_board = chess.Board()
    clock = pygame.time.Clock()
    running = True
    move_made = None
    
    sound_manager = SoundManager()

    redraw_needed = True

    while running:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT: # chiudere finestra = quit
                running = False

            #al click registro gestisco mossa
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked_square = get_square_under_mouse(pygame.mouse.get_pos())
                move_made = handle_move(chess_board, move_made, clicked_square, sound_manager)
                redraw_needed = True    

        #quit se GameOver
        if check_game_over(chess_board):
                running = False
        
        # Draw vari
        if redraw_needed:
            draw_board(screen)
            draw_selected_square(screen, move_made)
            draw_pieces(screen, chess_board, font)
            pygame.display.flip()
            redraw_needed = False

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()  