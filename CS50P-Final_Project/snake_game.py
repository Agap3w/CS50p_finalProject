import pygame, sys, random, sqlite3
from pygame.math import Vector2 

# GameManager
class GameManager:
    def __init__(self):
        self.username = self.get_username()

    def get_username(self):
        username = ""  # Initialize username as an empty string
        active = True  # Whether the input box is active
        input_box = pygame.Rect(100, 200, 400, 50)
        font = pygame.font.Font(None, 32)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive

        while active:
            screen.fill((30, 30, 30))  # Background color for the prompt

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Press Enter to confirm
                        active = False  # Exit the input loop
                    elif event.key == pygame.K_BACKSPACE:  # Remove last character
                        username = username[:-1]
                    else:
                        username += event.unicode  # Add typed character to username

            pygame.draw.rect(screen, color, input_box, 2)
            text_surface = font.render(username.upper(), True, pygame.Color('white'))
            screen.blit(text_surface, (input_box.x + 10, input_box.y + 10))
            input_box.w = max(400, text_surface.get_width() + 20)  # Adjust width dynamically

            prompt_surface = font.render("Enter your name and press \"Enter\"", True, pygame.Color('white'))
            screen.blit(prompt_surface, (100, 150))
            pygame.display.flip()
            clock.tick(30)  # Limit frame rate

        return username.upper()

    def insert_score(self, score):
        with sqlite3.connect('snake.db') as db:
            db.execute('INSERT INTO scores (username, score) VALUES (?, ?)', (self.username, score))

    #prendo dato record utente corrente
    def get_high_score(self):
        with sqlite3.connect('snake.db') as db:
            cursor = db.cursor()
            cursor.execute("SELECT MAX(score) FROM scores WHERE username = ?", (self.username,))
            result = cursor.fetchone()
            return result[0] if result[0] else 0

    # prendo dati per hall of fame
    def get_high_scores(self, limit=5):
        with sqlite3.connect('snake.db') as db:
            cursor = db.cursor()
            cursor.execute(
                'SELECT username, MAX(score) as best_score FROM scores GROUP BY username ORDER BY best_score DESC LIMIT ?',
                (limit,)
            )
            return cursor.fetchall()
    
    def get_previous_best_score(self):
        with sqlite3.connect('snake.db') as db:
            cursor = db.cursor()
            cursor.execute('SELECT MAX(score) FROM scores WHERE username = ?', (self.username,))
            result = cursor.fetchone()
            return result[0] if result and result[0] else 0

#il serpente
class SNAKE: 
    def __init__(self):
        self.body = [Vector2(5,11), Vector2(4,11), Vector2(3,11)] 
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
        self.y = random.randint(1,cell_number)
        self.pos = Vector2(self.x, self.y)
    
    
    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x*cell_size, self.pos.y*cell_size, cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0,cell_number-1)
        self.y = random.randint(1,cell_number)
        self.pos = Vector2(self.x, self.y)

#MAIN (include GameManagerserpente + frutta + background + dinamiche di gioco come collisione e game_over)        
class MAIN:
    def __init__(self, game_manager):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.game_manager = game_manager  # Store reference to the game manager
        self.username = self.game_manager.username  # Fetch username from GameManager

        #initialize record-related attributes
        self.previous_best = self.game_manager.get_previous_best_score()  # Fetch player's best score
        self.new_record = False  # Track if a new record is in progress
        self.record_start_time = None  # Track when record notification starts
        self.record_sound = pygame.mixer.Sound("static/saetta.wav")  # Audio for new record
        self.record_sound_played = False  # New flag to track sound playback

        # Initialize animation-related attributes
        self.animation_active = False
        self.animation_start_time = 0
        self.animation_pos_x = -200  # Start off-screen
        self.animation_pos_y = (cell_number * cell_size + cell_size) // 2 - 50  # Centered Y position
        self.animation_speed = 6  # Adjust speed
        self.animation_cause = None  # Store cause

        
        self.animation_sound = pygame.mixer.Sound("static/sirena.wav")  # Add sound effect for ambulance and sheriff animations
    
    def update(self):
        if not self.animation_active and self.snake.direction != Vector2(0, 0):  # Only update if the snake is moving
            self.snake.move_snake()
            self.check_collision_and_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit() 
        self.snake.draw_snake()
        self.draw_titanPanel() 

    def check_collision_and_fail(self):
        head_pos = self.snake.body[0]

        # Check if snake collides with itself or walls
        if head_pos in self.snake.body[1:]:
            self.game_over(cause="collision")

        # Check if snake moves out of bounds
        elif not (0 <= head_pos.x < cell_number and 1 <= head_pos.y < cell_number + 1):
            self.game_over(cause="fail")

        # If snake eats the fruit, add block and play sound
        if self.fruit.pos == head_pos:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()
        
        # Check for new record
        current_score = len(self.snake.body) - 3
        if current_score > self.previous_best:  # Check if it's a new record
            if not self.record_sound_played:  # Play the sound only once
                self.record_sound.play()
                self.record_sound_played = True  # Prevent replaying during the same session
            self.new_record = True  # Indicate a new record is in progress
            self.record_start_time = pygame.time.get_ticks()  # Save the start time for the record animation
        else:
            self.new_record = False  # Reset if not a new record
            self.record_start_time = None

        #se frutta respawna su serpente, ripeto respawn
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()
    
    def get_high_score(self):
    #Fetch the current high score from the database.
        return self.game_manager.get_high_score()

    def game_over(self, cause):
        # Save the current score using GameManager
        current_score = len(self.snake.body) - 3
        self.game_manager.insert_score(current_score)

        # Update the previous_best dynamically after inserting the new score
        self.previous_best = self.game_manager.get_previous_best_score()    

        # Reset record-related attributes
        self.record_sound_played = False
        self.new_record = False  # Reset record flag
        self.record_start_time = None  # Reset record timing

        # Display game-over animation and message
        self.start_animation(cause)
        self.snake.reset()  # Reset the snake and game state

    def start_animation(self, cause):
        self.animation_active = True
        self.animation_pos_x = -200  # Start off-screen
        self.animation_start_time = pygame.time.get_ticks()  # Get current time for animation duration
        self.animation_cause = cause  # Set the cause of the animation (e.g., "collision" or "fail")
        self.animation_sound.play() # Play the sound when animation starts

    def update_animation(self):
        if self.animation_active:
            # Check if any key is pressed during the animation
            if (pygame.key.get_pressed()[pygame.K_SPACE]):
                self.animation_active = False  # Stop the animation
                self.snake.reset()  # Reset the snake immediately after the animation stops
                return

            elapsed_time = pygame.time.get_ticks() - self.animation_start_time
            if elapsed_time > 5000:  # Stop animation after 5 seconds
                self.animation_active = False
                self.snake.reset()  # Reset the snake after animation

            screen.fill((50, 50, 50))  # Clear the screen

            # Center position in the X-axis
            center_x = (cell_number * cell_size) // 3

            if self.animation_pos_x < center_x:  # Only move if the animation hasn't reached center
                self.animation_pos_x += self.animation_speed
            else:
                self.animation_pos_x = center_x  # Stop at the center

            if self.animation_cause == "collision":
                screen.blit(pygame.image.load("static/ambulanza.png"), (self.animation_pos_x, (cell_number+1)*cell_size//2 - 50))
                self.display_message("Ahia che male! AMBULANZA!", (255, 165, 0))
            elif self.animation_cause == "fail":
                screen.blit(pygame.image.load("static/sceriffo.png"), (self.animation_pos_x, (cell_number+1)*cell_size//2 - 50))
                self.display_message("Il serpente è scappato! SCERIFFO!", (255, 165, 0))

    def display_message(self, message, color):
        font = pygame.font.Font(None, 50)  # Choose font and size
        text_surface = font.render(message, True, color)
        text_rect = text_surface.get_rect(center=((cell_number*cell_size) // 2, (cell_number+1*cell_size) // 2 + 100))
        screen.blit(text_surface, text_rect)

    def wait_for_user_input_or_timeout(self):
        start_time = pygame.time.get_ticks()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    return
            if pygame.time.get_ticks() - start_time > 5000:  # 5 seconds timeout
                return

    def draw_grass(self):
        grass_colour = (135,170,60)
        for row in range(1, cell_number+1):
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

    def draw_titanPanel(self):
        # Draw score bar
        panel_frame_rect = pygame.Rect(0, 0, cell_size * cell_number, cell_size)  # Top row (20 cells wide)
        pygame.draw.rect(screen, (90, 90, 90), panel_frame_rect, 2)  # Grey border (2-pixel thick)

        current_score = len(self.snake.body) - 3  # Calculate current score
        high_score = self.get_high_score()  # Always fetch the latest high score

        if current_score > high_score:
            # New record is in progress
            if not self.new_record:
                self.new_record = True  # Set new record flag 

            pygame.draw.rect(screen, (255, 0, 0), panel_frame_rect)  # Red Titan Panel

            # Draw the "NEW RECORD IN PROGRESS" message
            record_surface = game_font.render(f"NEW RECORD IN PROGRESS: {current_score}", True, (255, 255, 255))
            screen.blit(record_surface, (panel_frame_rect.centerx - record_surface.get_width() // 2, 10))
            

        else:
            pygame.draw.rect(screen, (200, 200, 200), panel_frame_rect)  # Default gray Titan Panel

            # Draw the score text
            score_surface = game_font.render(str(current_score), True, (0, 0, 0))  # Black text
            score_x = cell_size * (cell_number // 2)  # Centered score
            score_y = cell_size // 2  # Vertically centered
            score_rect = score_surface.get_rect(midright=(score_x, score_y))
            screen.blit(score_surface, score_rect)  # Draw the score

            # Draw the apple icon
            apple_rect = apple.get_rect(midright=(score_rect.left - 10, score_rect.centery))  # 10px gap to the left of the score
            screen.blit(apple, apple_rect)  # Draw the apple icon

            # Draw the username
            username_surface = game_font.render(f"{self.username}", True, (0, 0, 0))
            screen.blit(username_surface, (50, 10))  # Display username at top-left

            # Draw the trophy icon
            trophy_rect = trophy.get_rect(midright=(panel_frame_rect.right - 40, score_rect.centery))  # 10px gap
            screen.blit(trophy, trophy_rect)
            self.trophy_button_rect = trophy_rect  # Add click detection for trophy

    def show_high_scores(self):
        popup_width = cell_size * 10
        popup_height = cell_size * 10
        popup_surface = pygame.Surface((popup_width, popup_height))
        popup_surface.fill((50, 50, 50))  # Dark gray background
        pygame.draw.rect(popup_surface, (200, 200, 200), popup_surface.get_rect(), 2)

        high_scores = self.game_manager.get_high_scores()  # Fetch from GameManager

        font = pygame.font.Font(None, 28)
        title_surface = font.render("I più bravi:", True, (255, 255, 255))
        popup_surface.blit(title_surface, (popup_width // 2 - title_surface.get_width() // 2, 20))

        y_offset = 60
        y_offset += 20  # Add extra space (this is the newline effect)

        for _, (user, score) in enumerate(high_scores):  # Ignore the index by using `_`
            score_text = f"{user}: {score}"  # Remove the number before the user
            score_surface = font.render(score_text, True, (255, 255, 255))
            popup_surface.blit(score_surface, (20, y_offset))
            y_offset += 40

        screen.blit(popup_surface, (cell_size * 5, cell_size * 5))
        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type in {pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN}:
                    waiting = False

pygame.init()

cell_size = 40
cell_number = 20

screen = pygame.display.set_mode((cell_number*cell_size, (cell_number+1)*cell_size)) 
clock = pygame.time.Clock()
apple = pygame.image.load("static/apple.png").convert_alpha()
trophy = pygame.image.load("static/coppa.png").convert_alpha()
game_font = pygame.font.Font(None, 25) #ARG = (font, fontsize). Come font posso usare 'None' oppure uploadare un '../static/font.ttf'

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

game_manager = GameManager()  # Initialize GameManager
main_game = MAIN(game_manager)  # Pass GameManager to MAIN

# Variable to track the time of the last input
last_input_time = 0
input_delay = 80  # 80 milliseconds delay between key presses

#game loop con quit option, screen_update e keybindings. background and draw elements
while True:

    current_time = pygame.time.get_ticks()  # Get current time in milliseconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if main_game.trophy_button_rect.collidepoint(event.pos):
                    main_game.show_high_scores()
 
        if event.type == SCREEN_UPDATE:
            main_game.update()

        if event.type == pygame.KEYDOWN:
            if current_time - last_input_time >= input_delay: # Only process input if enough time has passed since the last key press
                if event.key == pygame.K_UP and main_game.snake.direction.y != 1: 
                    main_game.snake.direction = Vector2(0,-1) 
                elif event.key == pygame.K_DOWN and main_game.snake.direction.y != -1: 
                    main_game.snake.direction = Vector2(0,1)
                elif event.key == pygame.K_LEFT and main_game.snake.direction.x != 1 and main_game.snake.direction != Vector2(0, 0):  # Can't move left if already moving right or if no direction
                    main_game.snake.direction = Vector2(-1, 0)
                elif event.key == pygame.K_RIGHT and main_game.snake.direction.x != -1: 
                    main_game.snake.direction = Vector2(1,0)
                # Update the last input time after processing the key press
                last_input_time = current_time

    screen.fill((145,182,63)) 
    main_game.draw_elements()
    main_game.update_animation()  # Run animation alongside other game elements
    pygame.display.update()
    clock.tick(60)