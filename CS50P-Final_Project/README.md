# CS50p_finalProject
## Snake Game

### Video Demo:  <URL HERE>
- - - -


### Description:
**Snake Game** is a python game for PC windows, developed with pygame library for both CS50p final project requirements and my son entertainment.
The game is a modern take on the classic Snake Game, enhanced with animations, sound effects, and a leaderboard feature.

#### Key Features:
- **Username & High Scores**: Players can input a username, which is used to track and store their scores in an SQL database.
- **Difficulty Levels**: Choose between `Easy` (slower snake movement) and `Hard` (faster gameplay).
- **Dynamic Gameplay**: 
  - The snake moves within a 20x20 grid, consuming apples to grow longer. 
  - An info panel at the top displays the current score, username, and a button to view the Hall of Fame.
  - The panel turns red if a new personal record is in progress.
- **Game Over**: 
  - Collision with walls or the snake itself triggers a game-over animation and sound effect. 
  - After 5 seconds (or upon skipping), the snake resets to its initial state, ready for a new match.
- **Hall of Fame**: View a leaderboard of the highest scores across all players.

#### Gameplay Overview:
The game opens in an 800x840 pixel window. The snake moves one grid cell at a time in four possible directions (up, down, left, right). When the snake eats an apple, it grows longer, and the apple respawns in a new location. The player’s score is equal to the number of apples consumed. Scores reset upon death.


### Code Structure:

#### **Helper Functions**:
1. **SQL Interactions**: Functions to fetch and store high scores in an SQLite database.
2. **Game Intro**: Manages the initial setup, allowing the user to input their username and select a difficulty mode.

#### **Classes**:
- **`Config`**: Holds constants for grid size, colors, screen dimensions, and other configurations.
- **`Snake`**: Handles snake movement, rendering, and growth mechanics when consuming fruits.
- **`Fruit`**: Manages the random positioning of fruits while avoiding overlap with the snake’s body.
- **`Game`**: The central class that integrates all components, including:
  - Collision detection.
  - High-score tracking and UI updates.
  - Animations for events like game-over and new records.
  - Sound effects for enhanced feedback.

#### **Main Function**:
The `main()` function initializes global variables and runs the game loop, which:
- Captures and processes user inputs.
- Updates the game state and snake’s movement.
- Renders game elements (snake, fruit, info panel).
- Handles animations and Hall of Fame interactions.


### References:
- [Get Started in Pygame in 10 minutes!](https://youtube.com/watch?v=y9VG3Pztok8) - 10min tutorial to introduce Pygame.
- [Learning pygame by creating Snake](https://youtube.com/watch?v=y9VG3Pztok8) - 2h tutorial to learn about Pygame throught a Snake-like game example.
- [CS50.ai](https://cs50.ai/chat) - specific doubt on small part of my code
- [GPT-4](https://chat.openai.com) - general feedback on my code 
- [Claude] (https://claude.ai/) - help with testing code
- [HiClipArt](https://www.hiclipart.com) - images db 
- [freesound](https://freesound.org/) - sound db