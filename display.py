from pygame.time import Clock
from pygame import Rect
import pygame
import random
class Display:
    RED = (255,0,0)
    BLUE = (0,0,255)
    BLACK = (0,0,0)
    SQUARE_PIX = 10
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
        self.dis = pygame.display.set_mode((width,height))
        pygame.display.set_caption("Snake Game")
        self.blue_rect = Rect(width//2, height//2, Display.SQUARE_PIX, Display.SQUARE_PIX)
        pygame.draw.rect(self.dis, Display.BLUE, self.blue_rect)
        pygame.display.update()
        red_l,red_t = self.rand_food_location()
        self.red_rect = Rect(red_l, red_t, Display.SQUARE_PIX, Display.SQUARE_PIX)
        pygame.draw.rect(self.dis, Display.RED, self.red_rect)
        pygame.display.update()
        self.fps_millis = 10
        self.pix_change = 5
        self.food_count = 0
        
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
        for dir in Display.DIRS:
            x = self.red_rect.left + dir[0]
            y = self.red_rect.top + dir[1]
            if not self.is_within_window(x,y):
                continue
            if self.dis.get_at((x,y)) == pygame.Color(Display.BLUE):
                return True
        return False

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
                print(self.dis.get_at((x,y)))
                # red square overwritten when blue moves on top
                if not self.is_within_window(x,y) or self.dis.get_at((x,y)) == pygame.Color(Display.BLUE):
                    valid_loc = False
                    break
            print(x,y)
        return (red_l,red_t)
    
    def update_food_loc(self):
        new_l, new_t = self.rand_food_location()
        self.red_rect.update(new_l, new_t, Display.SQUARE_PIX, Display.SQUARE_PIX)
        pygame.draw.rect(self.dis, Display.RED, self.red_rect)
        
    def game_loop(self):
        moved = False
        clk = Clock()
        game_over = False
        prev_move = (0,0)
        while not game_over:
            clk.tick(self.fps_millis)
            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    x,y = (0,0)
                    if event.key == pygame.K_LEFT:
                        x = -self.pix_change
                    elif event.key == pygame.K_RIGHT:
                        x = self.pix_change
                    elif event.key == pygame.K_DOWN:
                        y = self.pix_change
                    elif event.key == pygame.K_UP:
                        y = -self.pix_change
                    self.blue_rect.move_ip(x,y)
                    prev_move = (x,y)
                    moved = True
                else:
                    moved = False
            if not moved:
                self.blue_rect.move_ip(prev_move[0], prev_move[1])
            self.dis.fill(Display.BLACK)
            pygame.draw.rect(self.dis, Display.RED, self.red_rect)
            pygame.draw.rect(self.dis, Display.BLUE, self.blue_rect)
            print(self.dis.get_at((self.red_rect.left, self.red_rect.top)))
            if self.has_eaten_food():
                print("Food obtained")
                self.food_count += 1
                # update location
                self.update_food_loc()
            pygame.display.update()
            if self.blue_rect.left < 0 or self.blue_rect.right > self.width or self.blue_rect.top < 0 or self.blue_rect.bottom > self.height:
                game_over = True
        print("Goodbye")
        pygame.quit()
        quit()

if __name__ == "__main__":
    disp = Display(600, 300)
    disp.game_loop()
