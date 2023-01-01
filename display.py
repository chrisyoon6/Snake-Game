from pygame.time import Clock
from pygame import Rect
from pygame import font
import pygame
import random
from enum import Enum
from collections import deque
from copy import copy
import json
import os

class Orientation(Enum):
    none = -1
    up = 0
    right = 1
    down = 2
    left = 3

class Status(Enum):
    dormat = -1
    quit = 0
    play = 1

class Display:
    RED = (255,0,0)
    BLUE = (0,0,255)
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    SQUARE_PIX = 20
    FONT_SIZE = 30
    SCORES_FONT_SIZE = 30
    FPS_MILLIS = 10
    """For left, top corner as reference pt"""
    DIRS = [[0,0], [SQUARE_PIX,0], [SQUARE_PIX, SQUARE_PIX], [0, SQUARE_PIX]]
    def __init__(self, width, height) -> None:
        """Initializes a Display object.

        Args:
            width (int): width of the display
            height (int): height of the display
        """        
        pygame.init()
        self.width = width
        self.height = height
        self.fps_millis = Display.FPS_MILLIS
        self.pix_change = Display.SQUARE_PIX
        self.font = font.SysFont("arial", Display.FONT_SIZE)
        self.scores_font = font.SysFont("arial", Display.SCORES_FONT_SIZE)
        self.keep_playing = True
        self.dis = None
        self.snake = None
        self.snake_head = None
        self.snake_rects = None
        self.red_rect = None
        self.food_count = None
        self.orient = None
        self.scores = {}

    def initiate_game(self):
        """Initiates the Snake Game
        """        
        self.dis = pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption("Snake Game")
        """List of tuples representing the top left corner of each rectangle component the snake."""
        self.snake = deque([(self.width//2, self.height//2)])
        self.snake_head = Rect(self.width//2, self.height//2, Display.SQUARE_PIX, Display.SQUARE_PIX)
        self.snake_rects = [self.snake_head]
        pygame.draw.rect(self.dis, Display.BLUE, self.snake_head)
        red_l,red_t = self.rand_food_location()
        self.red_rect = Rect(red_l, red_t, Display.SQUARE_PIX, Display.SQUARE_PIX)
        pygame.draw.rect(self.dis, Display.RED, self.red_rect)
        self.food_count = 0
        self.orient = Orientation.none
        self.scores = {}

    def is_within_window(self, x, y) -> bool:
        """Determines if the coordinates are within the defined window size

        Args:
            x (int): x coordinate of the pixel
            y (int): y coordinate of the pixel

        Returns:
            bool: True if both x,y coordinates are within the window size
        """        
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    def has_eaten_food(self) -> bool:
        """Determines whether or not the snake has eaten food.

        Returns:
            bool: True if the snake is at the food's location at the time of the method call
        """
        return self.red_rect.colliderect(self.snake_head)

    def rand_food_location(self) -> tuple[int,int]:
        """Returns a valid random location for the red rectangle (food) to spawn.

        Returns:
            tuple[int,int]: x,y coordinates of the top left part of the rectangle.
        """        
        valid_loc = False
        red_l = 0
        red_t = 0
        while not valid_loc:
            red_l = random.randint(0, self.width-Display.SQUARE_PIX)
            red_t = random.randint(0, self.height-Display.SQUARE_PIX)
            # all dims of red square
            valid_loc = True
            for dir in Display.DIRS:
                x = red_l + dir[0]
                y = red_t + dir[1]
                # red square overwritten when blue moves on top
                if not self.is_within_window(x,y) or self.dis.get_at((x,y)) == pygame.Color(Display.BLUE):
                    valid_loc = False
                    break
        return (red_l,red_t)
    
    def update_food_loc(self) -> None:
        """Updates location of the food. To be called after food is obtained.
        """        
        new_l, new_t = self.rand_food_location()
        self.red_rect.update(new_l, new_t, Display.SQUARE_PIX, Display.SQUARE_PIX)
        pygame.draw.rect(self.dis, Display.RED, self.red_rect)

    def update_snake(self, has_eaten_food):
        """Updates the snake's chain of rectangles

        Args:
            has_eaten_food (bool): True if snake has eaten food at the time of the method call
        """        
        self.snake.appendleft((self.snake_head.left, self.snake_head.top))
        self.snake_rects.insert(0, copy(self.snake_head))
        if not has_eaten_food:
            self.snake.pop()
            self.snake_rects.pop()

    def display_snake(self):
        """Displays the current snake on the screen
        """        
        for cmp in self.snake_rects:
            pygame.draw.rect(self.dis, Display.BLUE, cmp)

    def update_display(self):
        """Updates the screen with the game's current state
        """        
        self.dis.fill(Display.BLACK)
        pygame.draw.rect(self.dis, Display.RED, self.red_rect)
        score_label = self.font.render("Score: " + str(self.food_count), True, Display.WHITE)
        self.dis.blit(score_label, (0,0))
        self.display_snake()    

    def has_collided(self) -> bool:
        """Determines whether or not the snake has collied with itself

        Returns:
            bool: True if collison occurred, False otherwise.
        """        
        if self.snake_head.collidelist(self.snake_rects[1:]) != -1:
            return True
        return False

    def update_scores(self):
        """Displays the highest scores from this game. To be called when the game has ended.
        """     
        scores = {}
        count = 0
        with open("scores.json", "r") as f:
            if os.stat("scores.json").st_size != 0:
                scores = f.read()
                scores = json.loads(scores)
                count = int(list(scores.keys())[-1]) + 1
        with open("scores.json", "w") as f:
            scores[str(count)] = str(self.food_count)
            json.dump(scores, f)
        self.scores = scores

    def display_highscores(self, nums=5):
        """Displays the top scores of the game.

        Args:
            nums (int, optional): _description_. Defaults to 5.
        """        
        scores = list(self.scores.values())
        scores.sort(reverse=True)
        if nums > len(scores):
            nums = len(scores)
        scores = scores[:nums]
        scores_str = "High scores: "
        for s in scores:
            scores_str += str(s) + " "
        scores_label = self.scores_font.render(scores_str, True, Display.WHITE)
        curr_score_label = self.scores_font.render("Your score: " + str(self.food_count), True, Display.WHITE)
        options_label = self.scores_font.render("Press \'c\' to play again", True, Display.WHITE)
        self.dis.blits(blit_sequence=((scores_label, (0,0)), (curr_score_label, (0, int(self.height*1/4))), (options_label, (0,int(self.height*3/4)))))
        pygame.display.update()

    def endgame_handler(self):
        """Handles anything that should occur once the game is over.

        Returns:
            Status: the status of the game, selected by the user
        """                
        self.display_highscores()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return Status.quit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                return Status.play
        return Status.dormat

    def game_loop(self):
        """Executes the Snake game
        """        
        while self.keep_playing:
            self.initiate_game()
            self.keep_playing = self.in_game_handler() == Status.play
        pygame.quit()
        quit()
        
    def in_game_handler(self):
        """Handles all in-game events

        Returns:
            Status: Whether the user has quit the game or wants to play again
        """        
        clk = Clock()
        game_over = False
        close_app = False
        prev_move = (0,0)            
        while True:
            if game_over:
                status = self.endgame_handler()
                if status == Status.dormat:
                    continue
                return status

            clk.tick(self.fps_millis)
            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    x,y = (0,0)
                    if event.key == pygame.K_LEFT:
                        x = -self.pix_change
                        self.orient = Orientation.left
                    elif event.key == pygame.K_RIGHT:
                        x = self.pix_change
                        self.orient = Orientation.right
                    elif event.key == pygame.K_DOWN:
                        y = self.pix_change
                        self.orient = Orientation.down
                    elif event.key == pygame.K_UP:
                        y = -self.pix_change
                        self.orient = Orientation.up
                    prev_move = (x,y)
                break
            self.snake_head.move_ip(prev_move[0], prev_move[1])
            has_eaten = False
            if self.has_eaten_food():
                print("Food obtained")
                self.food_count += 1
                # update location
                self.update_food_loc()
                has_eaten = True
            self.update_snake(has_eaten)
            self.update_display()
            if self.snake_head.left < 0 or self.snake_head.right > self.width or self.snake_head.top < 0 or self.snake_head.bottom > self.height:
                print("Out of bounds!")
                game_over = True
                self.dis.fill(Display.BLACK)
                self.update_scores()  
            elif not has_eaten and self.has_collided():
                print(self.snake)
                print("Collided!")
                game_over = True
                self.dis.fill(Display.BLACK)
                self.update_scores()  

            pygame.display.update()

def json_test():
    scores = {}
    with open("scores.json", "r") as f:
        if os.stat("scores.json").st_size != 0:
            scores = f.read()
            scores = json.loads(scores)
    print(type(scores))
    with open("scores.json", "w") as f:
        scores['player2'] = str(2)
        json.dump(scores, f)
    print(str(scores))
if __name__ == "__main__":
    # json_test()
    disp = Display(300, 300)
    disp.game_loop()
