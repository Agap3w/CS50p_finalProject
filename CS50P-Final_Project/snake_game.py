import pygame, sys, random, sqlite3
from pygame.math import Vector2 

# Function to prompt for username
def get_username():
    username = ""  # Initialize username as an empty string
    active = True  # Whether the input box is active

    input_box = pygame.Rect(100, 200, 400, 50)  # Input box dimensions
    font = pygame.font.Font(None, 32)  # Font for the username
    color_inactive = pygame.Color('lightskyblue3')  # Box color (inactive)
    color_active = pygame.Color('dodgerblue2')  # Box color (active)
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

        # Draw the input box
        pygame.draw.rect(screen, color, input_box, 2)
        text_surface = font.render(username, True, pygame.Color('white'))
        screen.blit(text_surface, (input_box.x + 10, input_box.y + 10))
        input_box.w = max(400, text_surface.get_width() + 20)  # Adjust width dynamically

        # Display prompt text
        prompt_surface = font.render("Enter your username and press Enter:", True, pygame.Color('white'))
        screen.blit(prompt_surface, (100, 150))

        pygame.display.flip()
        clock.tick(30)  # Limit frame rate

    return username

def insert_score(username, score):
    with sqlite3.connect('snake.db') as db:
        db.execute('INSERT INTO scores (username, score) VALUES (?, ?)', (username, score))

def get_high_score(username):
    with sqlite3.connect('snake.db') as db:
        cursor = db.cursor()
        cursor.execute('SELECT MAX(score) FROM scores WHERE username = ?', (username,))
        high_score = cursor.fetchone()[0]
    return high_score if high_score is not None else 0

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
        self.y = random.randint(0,cell_number-1)
        self.pos = Vector2(self.x, self.y)
    
    
    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x*cell_size, self.pos.y*cell_size, cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0,cell_number-1)
        self.y = random.randint(1,cell_number)
        self.pos = Vector2(self.x, self.y)

#MAIN (include serpente + frutta + background + dinamiche di gioco come collisione e game_over)        
class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.username = get_username()  # Ask for the username
    
    def update(self):
        self.snake.move_snake() 
        self.check_collision_and_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit() 
        self.snake.draw_snake()
        self.draw_score() 

    def check_collision_and_fail(self):
        head_pos = self.snake.body[0]

        # Check if snake collides with itself or walls
        if not (0 <= head_pos.x < cell_number and 1 <= head_pos.y < cell_number + 1) or head_pos in self.snake.body[1:]:
            self.game_over()

        # If snake eats the fruit, add block and play sound
        if self.fruit.pos == head_pos:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()

        #se frutta respawna su serpente, ripeto respawn
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()
    
    def game_over(self):
        self.snake.reset()  # Reset the snake and game state

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

    def draw_score(self):
        # Calculate the dimensions and position of the score frame
        score_frame_rect = pygame.Rect(0, 0, cell_size * cell_number, cell_size)  # Top row (20 cells wide)
        
        # Draw the background of the score frame
        pygame.draw.rect(screen, (200, 200, 200), score_frame_rect)  # Greenish background
        pygame.draw.rect(screen, (90, 90, 90), score_frame_rect, 2)  # Grey border (2-pixel thick)

        # Render the score text
        score_text = str(len(self.snake.body) - 3)  # Calculate score
        score_surface = game_font.render(score_text, True, (0, 0, 0))  # Black text

        # Position the score text in the frame
        score_x = cell_size * (cell_number - 2)  # 2 cells away from the right edge
        score_y = cell_size // 2  # Center vertically within the row
        score_rect = score_surface.get_rect(midright=(score_x, score_y))

        # Position the apple icon next to the score
        apple_rect = apple.get_rect(midright=(score_rect.left - 10, score_rect.centery))  # 10px gap to the left of the score

        # You can now display the username here if needed, e.g., at the top
        username_surface = game_font.render(f"{self.username}", True, (0, 0, 0))
        screen.blit(username_surface, (50, 10))  # Display username at top-left

        # Blit the elements onto the screen
        screen.blit(score_surface, score_rect)  # Draw the score
        screen.blit(apple, apple_rect)  # Draw the apple icon



pygame.init()

cell_size = 40
cell_number = 20

screen = pygame.display.set_mode((cell_number*cell_size, (cell_number+1)*cell_size)) 
clock = pygame.time.Clock()
apple = pygame.image.load("static/apple.png").convert_alpha()
game_font = pygame.font.Font(None, 25) #ARG = (font, fontsize). Come font posso usare 'None' oppure uploadare un '../static/font.ttf'

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN() 

#game loop con quit option, screen_update e keybindings. background and draw elements
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
 
        if event.type == SCREEN_UPDATE:
            main_game.update() 

        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_UP and main_game.snake.direction.y != 1: 
                main_game.snake.direction = Vector2(0,-1) 
            if event.key == pygame.K_DOWN and main_game.snake.direction.y != -1: 
                main_game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_LEFT and main_game.snake.direction.x != 1: 
                main_game.snake.direction = Vector2(-1,0)
            if event.key == pygame.K_RIGHT and main_game.snake.direction.x != -1: 
                main_game.snake.direction = Vector2(1,0)

    screen.fill((145,182,63)) 
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)