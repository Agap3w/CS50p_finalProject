import pygame, sys, random, sqlite3
from pygame.math import Vector2 

# Helpers functions
def get_username():
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

def insert_score(username, score):
    with sqlite3.connect('snake.db') as db:
        db.execute('INSERT INTO scores (username, score) VALUES (?, ?)', (username, score))

def extract_hall_of_fame():
    with sqlite3.connect('snake.db') as db:
        cursor = db.cursor()
        cursor.execute("SELECT username, MAX(score) as best_score FROM scores GROUP BY username ORDER BY best_score DESC LIMIT ?", (5,))
        return cursor.fetchall()

class Config:
    CELL_SIZE = 40
    CELL_NUMBER = 20
    SCREEN_WIDTH = CELL_NUMBER * CELL_SIZE
    SCREEN_HEIGHT = (CELL_NUMBER + 1) * CELL_SIZE
    BACKGROUND_COLOR = (145, 182, 63)
    FPS = 60

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

        block_rects = [pygame.Rect(block.x * Config.CELL_SIZE, block.y * Config.CELL_SIZE, Config.CELL_SIZE, Config.CELL_SIZE) for block in self.body]

        for index, block_rect in enumerate(block_rects):
            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - self.body[index]
                following_block = self.body[index - 1] - self.body[index]

                if previous_block.x == following_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == following_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    # Check diagonals only once and use cached results
                    if previous_block.x == -1 and following_block.y == -1 or previous_block.y == -1 and following_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == 1 and following_block.y == 1 or previous_block.y == 1 and following_block.x == 1:
                        screen.blit(self.body_br, block_rect)
                    elif previous_block.x == -1 and following_block.y == 1 or previous_block.y == 1 and following_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and following_block.y == -1 or previous_block.y == -1 and following_block.x == 1:
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
        new_head = self.body[0] + self.direction
        self.body.insert(0, new_head)
        if not self.new_block:
            self.body.pop()
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
        self.x = random.randint(0,Config.CELL_NUMBER-1)
        self.y = random.randint(1,Config.CELL_NUMBER)
        self.pos = Vector2(self.x, self.y)

        self.fruit_rect = pygame.Rect(self.pos.x*Config.CELL_SIZE, self.pos.y*Config.CELL_SIZE, Config.CELL_SIZE, Config.CELL_SIZE)
    
    def draw_fruit(self):
        screen.blit(apple, self.fruit_rect)

    def respawn(self):
        self.x = random.randint(0,Config.CELL_NUMBER-1)
        self.y = random.randint(1,Config.CELL_NUMBER)
        self.pos = Vector2(self.x, self.y)

        self.fruit_rect = pygame.Rect(self.pos.x * Config.CELL_SIZE, self.pos.y * Config.CELL_SIZE, Config.CELL_SIZE, Config.CELL_SIZE)

#MAIN (include GameManagerserpente + frutta + background + dinamiche di gioco come collisione e game_over)        
class GAME:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.username = get_username()  # Fetch username from GameManager

        self.trophy = pygame.image.load("static/coppa.png").convert_alpha()
        
        #initialize record-related attributes
        self.myRecord = self.get_myRecord()  # Fetch player's best score
        self.new_record = False  # Track if a new record is in progress
        self.record_start_time = None  # Track when record notification starts
        self.record_sound = pygame.mixer.Sound("static/saetta.wav")  # Audio for new record
        self.record_sound_played = False  # New flag to track sound playback

        # Initialize animation-related attributes
        self.animation_active = False
        self.animation_start_time = 0
        self.animation_pos_x = -200  # Start off-screen
        self.animation_pos_y = (Config.SCREEN_WIDTH + Config.CELL_SIZE) // 2 - 50  # Centered Y position
        self.animation_speed = 6  # Adjust speed
        self.animation_cause = None  # Store cause

        
        self.animation_sound = pygame.mixer.Sound("static/sirena.wav")  # Add sound effect for ambulance and sheriff animations
    
    def update(self):
        if not self.animation_active and self.snake.direction != Vector2(0, 0):  # Only update if the snake is moving
            self.snake.move_snake()
            self.check_collision_and_fail()

    def get_myRecord(self):
        with sqlite3.connect('snake.db') as db:
            cursor = db.cursor()
            cursor.execute('SELECT MAX(score) FROM scores WHERE username = ?', (self.username,))
            result = cursor.fetchone()
            return result[0] if result and result[0] else 0
    
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
            return

        # Check if snake moves out of bounds
        if not (0 <= head_pos.x < Config.CELL_NUMBER and 1 <= head_pos.y < Config.CELL_NUMBER + 1):
            self.game_over(cause="fail")
            return

        # If snake eats the fruit, add block and play sound
        if self.fruit.pos == head_pos:
            self.fruit.respawn()
            self.snake.add_block()
            self.snake.play_crunch_sound()
        
        # Check for new record
        current_score = len(self.snake.body) - 3
        if current_score > self.myRecord:  # Check if it's a new record
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
                self.fruit.respawn()

    def game_over(self, cause):
        self.save_score()
        self.reset_game_state()
        self.start_animation(cause)

    def save_score(self):
        current_score = len(self.snake.body) - 3
        insert_score(self.username, current_score)
        self.myRecord = self.get_myRecord()

    def reset_game_state(self):
        self.snake.reset()
        self.record_sound_played = False
        self.new_record = False
        self.record_start_time = None

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

            screen.fill((50, 50, 50))

            # Center position in the X-axis
            if self.animation_pos_x < (Config.SCREEN_WIDTH // 3):
                self.animation_pos_x += self.animation_speed
            else:
                self.animation_pos_x = Config.SCREEN_WIDTH // 3  # Stop at center

            if self.animation_cause == "collision":
                screen.blit(pygame.image.load("static/ambulanza.png"), (self.animation_pos_x, Config.SCREEN_HEIGHT//2 - 50))
                self.display_message("Ahia che male! AMBULANZA!", (255, 165, 0))
            elif self.animation_cause == "fail":
                screen.blit(pygame.image.load("static/sceriffo.png"), (self.animation_pos_x, Config.SCREEN_HEIGHT//2 - 50))
                self.display_message("Il serpente è scappato! SCERIFFO!", (255, 165, 0))

    def display_message(self, message, color):
        font = pygame.font.Font(None, 50)  # Choose font and size
        text_surface = font.render(message, True, color)
        text_rect = text_surface.get_rect(center=((Config.SCREEN_WIDTH) // 2, 200))
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
        grass_colour = (135, 170, 60)
        for row in range(1, Config.CELL_NUMBER + 1):
            for col in range(Config.CELL_NUMBER):
                if (row + col) % 2 == 0:
                    grass_rect = pygame.Rect(col * Config.CELL_SIZE, row * Config.CELL_SIZE, Config.CELL_SIZE, Config.CELL_SIZE)
                    pygame.draw.rect(screen, grass_colour, grass_rect)

    def draw_titanPanel(self):
        # Draw score bar
        panel_frame_rect = pygame.Rect(0, 0, Config.SCREEN_WIDTH, Config.CELL_SIZE)  # Top row (20 cells wide)
        pygame.draw.rect(screen, (90, 90, 90), panel_frame_rect, 2)  # Grey border (2-pixel thick)

        current_score = len(self.snake.body) - 3  # Calculate current score
        myRecord = self.get_myRecord()  # Always fetch the latest high score

        if current_score > myRecord:
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
            score_x = Config.CELL_SIZE * (Config.CELL_NUMBER // 2)  # Centered score
            score_y = Config.CELL_SIZE // 2  # Vertically centered
            score_rect = score_surface.get_rect(midright=(score_x, score_y))
            screen.blit(score_surface, score_rect)  # Draw the score

            # Draw the apple icon
            apple_rect = apple.get_rect(midright=(score_rect.left - 10, score_rect.centery))  # 10px gap to the left of the score
            screen.blit(apple, apple_rect)  # Draw the apple icon

            # Draw the username
            username_surface = game_font.render(f"{self.username}", True, (0, 0, 0))
            screen.blit(username_surface, (50, 10))  # Display username at top-left

            # Draw the trophy icon
            trophy_rect = self.trophy.get_rect(midright=(panel_frame_rect.right - 40, score_rect.centery))  # 10px gap
            screen.blit(self.trophy, trophy_rect)
            self.trophy_button_rect = trophy_rect  # Add click detection for trophy

    def show_hall_of_fame(self):
        popup_width = Config.CELL_SIZE * 10
        popup_height = Config.CELL_SIZE * 10
        popup_surface = pygame.Surface((popup_width, popup_height))
        popup_surface.fill((50, 50, 50))  # Dark gray background
        pygame.draw.rect(popup_surface, (200, 200, 200), popup_surface.get_rect(), 2)

        hall_of_fame = extract_hall_of_fame()  # Fetch from GameManager

        font = pygame.font.Font(None, 28)
        title_surface = font.render("I più bravi:", True, (255, 255, 255))
        popup_surface.blit(title_surface, (popup_width // 2 - title_surface.get_width() // 2, 20))

        y_offset = 60
        y_offset += 20  # Add extra space (this is the newline effect)

        for _, (user, score) in enumerate(hall_of_fame):  # Ignore the index by using `_`
            score_text = f"{user}: {score}"  # Remove the number before the user
            score_surface = font.render(score_text, True, (255, 255, 255))
            popup_surface.blit(score_surface, (20, y_offset))
            y_offset += 40

        screen.blit(popup_surface, (Config.CELL_SIZE * 5, Config.CELL_SIZE * 5))
        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type in {pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN}:
                    waiting = False

def main():
    pygame.init()

    global screen, clock, apple, game_font

    screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    apple = pygame.image.load("static/apple.png").convert_alpha()
    game_font = pygame.font.Font(None, 25)

    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 150)

    game = GAME()

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
                    if game.trophy_button_rect.collidepoint(event.pos):
                        game.show_hall_of_fame()
    
            if event.type == SCREEN_UPDATE:
                game.update()

            if event.type == pygame.KEYDOWN:
                if current_time - last_input_time >= input_delay: # Only process input if enough time has passed since the last key press
                    if event.key == pygame.K_UP and game.snake.direction.y != 1: 
                        game.snake.direction = Vector2(0,-1) 
                    elif event.key == pygame.K_DOWN and game.snake.direction.y != -1: 
                        game.snake.direction = Vector2(0,1)
                    elif event.key == pygame.K_LEFT and game.snake.direction.x != 1 and game.snake.direction != Vector2(0, 0):  # Can't move left if already moving right or if no direction
                        game.snake.direction = Vector2(-1, 0)
                    elif event.key == pygame.K_RIGHT and game.snake.direction.x != -1: 
                        game.snake.direction = Vector2(1,0)
                    # Update the last input time after processing the key press
                    last_input_time = current_time

        screen.fill(Config.BACKGROUND_COLOR) 
        game.draw_elements()
        game.update_animation()  # Run animation alongside other game elements
        pygame.display.update()
        clock.tick(Config.FPS)

if __name__ == "__main__":
    main()