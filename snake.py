# ------------------------------------------------
# Dateiname: snake.py
# Version: 1.0
# Funktion: Snake Game
# Autor: AP
# Datum der letzten Änderung: 18.01.2024
# ------------------------------------------------

# Modules used ----------------------------------------------------------------------------------------------------------

import pygame
import sys
import random
from pygame.math import Vector2
import time


# Definition of the classes ---------------------------------------------------------------------------------------------

class Food:
    def __init__(self):
        '''Draws the food and randomises its graphics and position.'''
        self.randomize_food()
         
    def draw_food(self):
        '''Draws the food within the grid pattern'''
        # position is multiplied by cell_size to maintain the grid pattern we created in the window
        x_pos = self.position.x * cell_size
        y_pos = self.position.y * cell_size
        food_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
        window.blit(self.food, food_rect)
         
    def randomize_food(self):
        '''Randomises the position at which the food will appear and the graphics of the food.'''
        # generates a random position, -1 ensures that the food is not outside the window
        self.x_pos = random.randint(0, cell_number - 1)
        self.y_pos = random.randint(0, cell_number - 1)
        # working with vectors in this case is easier than working with lists
        self.position = Vector2(self.x_pos, self.y_pos)

        # import food graphics
        self.apple = pygame.image.load(r'graphics\apple.png').convert_alpha()
        self.grapes = pygame.image.load(r'graphics\grapes.png').convert_alpha()
        self.watermelon = pygame.image.load(r'graphics\watermelon.png').convert_alpha()
        self.orange = pygame.image.load(r'graphics\orange.png').convert_alpha()
        self.strawberry = pygame.image.load(r'graphics\strawberry.png').convert_alpha()
        
        # randomises the food that appears
        self.food_list = [self.apple, self.grapes, self.watermelon, self.orange, self.strawberry]
        self.food = self.food_list[random.randint(0,len(self.food_list)-1)]

class Snake:
    '''Builds the snake and defines its movement and sounds'''
    def __init__(self):
        # creats the body of the snake with its starting position
        self.body = [Vector2(7,10), Vector2(6,10), Vector2(5,10)]
        # the direction in which the snake will automatically move without any input from the player
        self.direction = Vector2(1,0)
        self.new_block = False

        # imports the snakes images - convert_alpha() so that Python can work with the image more easily.
        self.snake_head_up = pygame.image.load(r'graphics\head_up.png').convert_alpha()
        self.snake_head_down = pygame.image.load(r'graphics\head_down.png').convert_alpha()
        self.snake_head_left = pygame.image.load(r'graphics\head_left.png').convert_alpha()
        self.snake_head_right = pygame.image.load(r'graphics\head_right.png').convert_alpha()

        self.snake_body_horizontal = pygame.image.load(r'graphics\body_hor.png').convert_alpha()
        self.snake_body_vertical = pygame.image.load(r'graphics\body_vert.png').convert_alpha()
        self.snake_body_bow_tr = pygame.image.load(r'graphics\bow_tr.png').convert_alpha()
        self.snake_body_bow_tl = pygame.image.load(r'graphics\bow_tl.png').convert_alpha()
        self.snake_body_bow_br = pygame.image.load(r'graphics\bow_br.png').convert_alpha()
        self.snake_body_bow_bl = pygame.image.load(r'graphics\bow_bl.png').convert_alpha()

        self.snake_tail_up = pygame.image.load(r'graphics\tail_up.png').convert_alpha()
        self.snake_tail_down = pygame.image.load(r'graphics\tail_down.png').convert_alpha()
        self.snake_tail_left = pygame.image.load(r'graphics\tail_left.png').convert_alpha()
        self.snake_tail_right = pygame.image.load(r'graphics\tail_right.png').convert_alpha()

        # adds the sound effect for eating food and failing
        self.eating_sound = pygame.mixer.Sound(r'sounds\eating.mp3')
        self.fail_sound = pygame.mixer.Sound(r'sounds\doh.mp3')
   
    def draw_snake(self):
        '''Draws the snake on the screen according to the first created grid pattern and selects the correct body image depending on how the snake moves.'''
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            # position is multiplied by cell_size to maintain the grid pattern we created in the window
            x_pos = block.x * cell_size
            y_pos = block.y * cell_size
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            
            # first block of the snake is its head, las one its tail
            if index == 0:
                window.blit(self.snake_head, block_rect)
            elif index == len(self.body) -1:
                window.blit(self.snake_tail, block_rect)
            # adds the body blocks depending on whether the snake runs horizontally or vertically
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index -1] - block
                if previous_block.x == next_block.x:
                    window.blit(self.snake_body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    window.blit(self.snake_body_horizontal, block_rect)
                # adds the corners of the snake when its changing directions
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        window.blit(self.snake_body_bow_tl, block_rect)
                    if previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        window.blit(self.snake_body_bow_br, block_rect)
                    if previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == +1:
                        window.blit(self.snake_body_bow_tr, block_rect)
                    if previous_block.x == -1 and next_block.y == 1 or previous_block.y == +1 and next_block.x == -1:
                        window.blit(self.snake_body_bow_bl, block_rect)

    def update_head_graphics(self):
        '''Updates the head graphics depending on the direction the snake is moving.'''
        # relation between the head and the block after it to update the heads direction
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0):
            self.snake_head = self.snake_head_left
        elif head_relation == Vector2(-1,0):
            self.snake_head = self.snake_head_right
        elif head_relation == Vector2(0,-1):
            self.snake_head = self.snake_head_down
        elif head_relation == Vector2(0,1):
            self.snake_head = self.snake_head_up

    def update_tail_graphics(self):
        '''Updates the tail graphics depending on the direction the snake is moving.'''
        # relation between the tail and the block before it to update the tails direction
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0):
            self.snake_tail = self.snake_tail_right
        elif tail_relation == Vector2(-1,0):
            self.snake_tail = self.snake_tail_left
        elif tail_relation == Vector2(0,-1):
            self.snake_tail = self.snake_tail_up
        elif tail_relation == Vector2(0,1):
            self.snake_tail = self.snake_tail_down

    def snake_movement(self):
        '''Moves the snake and adds a block if the conditions are '''
        if self.new_block == True:
            # copies the whole body
            body_copy = self.body[:]
            # adds the head depending on the direction
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            # must be set to false again, otherwise the snake would expand infinitely
            self.new_block = False
        else:    
            # shifts the body one position forward, removes the last position and adds the head of the snake, depending on the direction it goes
            # removes the last position
            body_copy = self.body[:-1]
            # adds the head depending on the direction
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        '''Adds a new block to the snake'''
        self.new_block = True
    
    def play_eating_sound(self):
        '''Plays eaiting sound.'''
        self.eating_sound.play()
            
    def play_fail_sound(self):
        '''Plays failure sound.'''
        self.fail_sound.play()

    def reset(self):
        '''Resets the snake's position and direction'''
        self.body = [Vector2(3,10), Vector2(2,10), Vector2(1,10)]
        self.direction = Vector2(1,0)


class Main:
    '''Draws and updates the elements, implements the score and game mechanics like collision and fail checks.'''
    def __init__(self):
        # instances of the other classes
        self.snake = Snake()
        self.food = Food()

    def update(self):
        '''Updates movement, collision and fail check every frame.'''
        self.snake.snake_movement()
        self.collision()
        self.failcheck()

    def draw_elements(self):
        '''Draws the elements on the screen.'''
        self.draw_ground()
        self.food.draw_food()
        self.snake.draw_snake()
        self.draw_score()
        
    def collision(self):
        '''Checks that the snake's head does collide with food. if it does, a sound is played, a block is added to the snake and new food is placed. 
            Also checks that no food is placed inside the snake's body. '''
        if self.food.position == self.snake.body[0]:
            # repositions food
            self.food.randomize_food()   
            self.snake.play_eating_sound()         
            # adds a block to the snake
            self.snake.add_block()
        # if the food spawns in the snakes body, it will spawn again at another position
        for block in self.snake.body[1:]:
            if block == self.food.position:
                self.food.randomize_food()

    def failcheck(self):
        '''Checks whether the snake fails by leaving the screen or colliding with its own body. If so, it plays a sound and the game restarts.'''
        # checks whether the head of the snake is outside the window
        if not 0 <= self.snake.body[0].x < cell_number:
            self.snake.play_fail_sound()
            time.sleep(1)
            # self.gameover()
            self.snake.reset()
        if not 0 <= self.snake.body[0].y < cell_number:
            self.snake.play_fail_sound()
            time.sleep(1)
            # self.gameover()
            self.snake.reset()
        # check if the snake hits itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0] and self.snake.direction != (0,0):
                self.snake.play_fail_sound()
                time.sleep(1)
                # self.gameover()
                self.snake.reset()

    def gameover(self):
        '''Ends the game.'''
        pygame.quit()
        sys.exit()
    
    def draw_ground(self):
        '''Adds a checkerboard grass pattern.'''
        grass_colour = (167,209,61)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(window, grass_colour, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(window, grass_colour, grass_rect)

    def draw_score(self):
        '''Adds a score to the bottom right corner of the screen, which counts each additional block of the snake.'''
        # is the length of the snake minus the 3 blocks with which it starts the game
        score_text = 'Score: ' + str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56,74,12))
        score_x_pos = int(cell_size * cell_number - 80)
        score_y_pos = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x_pos, score_y_pos))
        bg_rect = pygame.Rect(score_rect.left -7, score_rect.top -7 , score_rect.width +14, score_rect.height +14)        
        pygame.draw.rect(window, (167,209,61), bg_rect)
        pygame.draw.rect(window, (56,74,12), bg_rect, 2)
        window.blit(score_surface, score_rect)
        
# Definition of variables ----------------------------------------------------------------------------------------------
        
# improves sound output (44100 Hz, 16bit, stereo, buffer)
pygame.mixer.pre_init(44100,-16,2,512)
# initiates pygame
pygame.init()
cell_size = 40
cell_number = 20
window_width = 400
window_height = 500
framerate = 60

# Multiply cell_number by cell_size to create a grid pattern we need to build the snake
window = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()
game_font = pygame.font.Font(r'fonts\Mabook.ttf', 25)

# event automates snake's movement
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150) # milliseconds


main_game = Main()


# Game Loop ------------------------------------------------------------------------------------------------------------

while True:

    # event loop
    for event in pygame.event.get():
        # close game
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        # automatic snake movement and collision check
        if event.type == SCREEN_UPDATE:
            main_game.update()
        # directs the snake + another if statement to make sure the snake can't reverse itself   
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
     

    window.fill((175,215,70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(framerate)