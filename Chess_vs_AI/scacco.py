# TO DO:
# aggiungo promo choice

# MINOR:
# aggiungere pulsante per arrendersi / chiedere la patta
# sistemo grafica intro e outro

# VERY MINOR:
# customizzo grafica pezzi
# Move Highlighting: Show legal moves for the selected piece NB attivo solo dopo mossa irregolare
# Piece Capturing Animation (Optional): Provide visual feedback for captures. gIdea= barra nera laterale in cui scorrono dal basso verso l'alto gli "spiriti" dei pezzi, con le ali che flappano e un breve bubble text tipo "was I a good {piece}" 

# DOUBT:
# sql

import pygame
import chess
from constants import DIMENSION, SQUARE_SIZE, WIDTH, HEIGHT, LIGHT_COLOR, DARK_COLOR, UNICODE_PIECES, FPS

class ChessGame:
    def __init__(self):
        self.gui = GUI()
        self.sound_manager = SoundManager()
        self.game_logic = GameLogic()
        self.running = True
        self.gui.init_game()
        self.clock = pygame.time.Clock()  # Initialize the clock
        self.game_state = "intro"

    def main_game_loop(self):        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game_state == "intro":
                        play_button = self.gui.get_play_button_rect()
                        if play_button.collidepoint(event.pos):
                            self.game_state = "playing"
                            self.gui.redraw_needed = True

                    elif self.game_state == "playing":
                        move_info = self.game_logic.process_click(event.pos)
                        if move_info["move"]:       
                            self.sound_manager.play_move_sounds(move_info["move"], move_info["captured_piece"], move_info["is_check"])
                            self.gui.redraw_needed = True
                        if self.game_logic.is_game_over():
                            self.game_state = "outro"
                            self.gui.redraw_needed = True
                    
                    elif self.game_state == "outro":
                        retry_button = self.gui.get_retry_button_rect()
                        if retry_button.collidepoint(event.pos):
                            self.game_state = "intro"
                            self.game_logic = GameLogic()  # Reset game
                            self.gui.redraw_needed = True

            # Update the GUI (draw the board, pieces, selected square)
            if self.gui.redraw_needed:
                if self.game_state == "intro":
                    self.gui.draw_intro()
                elif self.game_state == "playing":
                    self.gui.draw_board()
                    self.gui.draw_selected_square(self.game_logic.selected_square)
                    self.gui.draw_pieces(self.game_logic.board)
                elif self.game_state == "outro":
                    self.gui.draw_outro()
                
                self.gui.refresh_display()  # Update the display
                self.gui.redraw_needed = False  

            # Keep the game running at the correct frame rate
            self.clock.tick(FPS)

class GUI:
    def __init__(self):
        self.screen = None
        self.font = None
        self.redraw_needed = True
        self.play_button_rect = None
        self.retry_button_rect = None
    
    def init_game(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess vs AI")
        
        # Try different fonts
        try:
            self.font = pygame.font.SysFont('segoe ui symbol', 60)  # Windows
        except:
            try:
                self.font = pygame.font.SysFont('arial unicode ms', 60)  # Alternative
            except:
                self.font = pygame.font.Font(None, 60)  # Fallback
        
        # Draw initial board
        self.draw_intro()
        self.refresh_display()

    def get_play_button_rect(self):
        return pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 50)
    
    def get_retry_button_rect(self):
        return pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 50)

    def draw_intro(self):
        self.screen.fill((0, 0, 0))
        text = self.font.render("Welcome to Chess", True, (255, 255, 255))
        self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        
        play_button = self.get_play_button_rect()
        pygame.draw.rect(self.screen, (0, 255, 0), play_button)
        button_text = self.font.render("Play", True, (255, 255, 255))
        self.screen.blit(button_text, (play_button.x + (play_button.width - button_text.get_width()) // 2, 
                                     play_button.y + (play_button.height - button_text.get_height()) // 2))

    def draw_outro(self):
        self.screen.fill((0, 0, 0))
        text = self.font.render("Game Over", True, (255, 0, 0))
        self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        
        retry_button = self.get_retry_button_rect()
        pygame.draw.rect(self.screen, (0, 255, 0), retry_button)
        button_text = self.font.render("Retry", True, (255, 255, 255))
        self.screen.blit(button_text, (retry_button.x + (retry_button.width - button_text.get_width()) // 2,
                                     retry_button.y + (retry_button.height - button_text.get_height()) // 2))

    def refresh_display(self):
        pygame.display.flip()
    
    def draw_board(self):
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                color = LIGHT_COLOR if (row + col) % 2 == 0 else DARK_COLOR
                pygame.draw.rect(self.screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    def draw_selected_square(self, square):
        if square is not None:  # If a square is selected
            col = chess.square_file(square)
            row = chess.square_rank(square)
            pygame.draw.rect(self.screen, (255, 255, 0, 50), 
                             pygame.Rect(col * SQUARE_SIZE, (7 - row) * SQUARE_SIZE, 
                                         SQUARE_SIZE, SQUARE_SIZE), 3)

    def draw_pieces(self, board=None):
        if board is None:
            board = chess.Board()  # Default to starting position if no board provided
        for square in chess.SQUARES:
            piece = board.piece_at(square)  # Get the piece at the given square
            if piece:  # If the piece exists
                piece_symbol = UNICODE_PIECES[piece.symbol()]  # Get the correct symbol for the piece
                col = chess.square_file(square)
                row = chess.square_rank(square)
                
                # Set the piece's color and render it on the screen
                color = (255, 255, 255) if piece.color else (0, 0, 0)
                text = self.font.render(piece_symbol, True, color)
                text_rect = text.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2, 
                                                  (7 - row) * SQUARE_SIZE + SQUARE_SIZE // 2))
                self.screen.blit(text, text_rect)
    
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

class GameLogic:
    def __init__(self):
        self.board = chess.Board()
        self.selected_square = None  # To store the currently selected square

    #converte posizione del mouse in square (per localizzare click?)
    def get_square_under_mouse(self, pos):
        x, y = pos
        col = x // SQUARE_SIZE
        row = 7 - (y // SQUARE_SIZE)
        return chess.square(col, row)
    
    #check per GameOver (incluso Stallo)
    def is_game_over(self):
        if self.board.is_checkmate():
            print("Checkmate!")
            return 1
        elif self.board.is_stalemate() or self.board.is_insufficient_material():
            print("Draw!")
            return 2
        return 0

    # Handle pawn promotion
    def is_promotion(self, piece, clicked_square):
        if piece and piece.piece_type == chess.PAWN:
            if (piece.color == chess.WHITE and chess.square_rank(clicked_square) == 7) or \
                (piece.color == chess.BLACK and chess.square_rank(clicked_square) == 0):
                    return True
        return False
    
    # helper function, return clicked square (da metter in helper appena riesco)
    def return_square(self, square=None, move=None, captured_piece=None, is_check=False, is_promotion=False):
        return {
            'selected_square': square,
            'move': move,
            'captured_piece': captured_piece,
            'is_check': is_check,
            'is_promotion': is_promotion
        }

    #al click ritorna un dict: {selected_square, move, captured_piece, is_check, is_promotion}
    def process_click(self, pos):
        clicked_square = self.get_square_under_mouse(pos) #prendo una square in base alla posiz del click del mouse
        piece = self.board.piece_at(clicked_square) #il pezzo su quella casella (if any)

        if self.selected_square is None: #se non avevo ancora una casella già selezionata
            if piece and piece.color == self.board.turn: # e su quella che scelgo c'è un pezzo del colore giusto
                self.selected_square = clicked_square # quella diventa la mia square selezionata
                return self.return_square(square=clicked_square) # e termino registrando la selezione
            return self.return_square() #se non c'è un pezzo eligible, termino con dict vuoto

        # (Else:) se invece ho già una selected_square
        current_piece = self.board.piece_at(self.selected_square)  #prendo pezzo che avevo selezionato
        
        if piece and piece.color == self.board.turn and clicked_square != self.selected_square: #se sto riselezionando un mio pezzo invece di muovere il precedente, accetto l'override
            self.selected_square = clicked_square # lo registro
            return self.return_square(square=clicked_square) #  e termino
        
        move = chess.Move(self.selected_square, clicked_square) # altrimenti, preparo la mossa
        
        #gestisco promozione pedone (per ora sempre in regina)
        if self.is_promotion(current_piece, clicked_square): 
            move = chess.Move(self.selected_square, clicked_square, promotion=chess.QUEEN)

        # Check if the move is legal
        if move in self.board.legal_moves:
            captured_piece = self.board.piece_at(clicked_square)
            self.board.push(move)
            self.selected_square = None
            return self.return_square(move=move, captured_piece=captured_piece, is_check=self.board.is_check(), is_promotion=self.is_promotion) 
            
        # If move is not legal, keep the selected square
        return self.return_square(square=self.selected_square)
    
def main():
    game = ChessGame()  # Create the ChessGame instance
    game.main_game_loop()  # Run the main game loop
    pygame.quit()  # Properly quit Pygame after the game loop ends

if __name__ == "__main__":
    main()  