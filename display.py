from pygame.time import Clock
from pygame import Rect
import pygame
import random
class Display:
    RED = (255,0,0)
    BLUE = (0,0,255)
    BLACK = (0,0,0)
    SQUARE_PIX = 10
    def __init__(self, width, height) -> None:
        """Initializes a Display object.

        Args:
            width (int): width of the display
            height (int): height of the display
        """        
        pygame.init()
        self.width = width
        self.height = height
        self.dis = pygame.display.set_mode((width,height), flags=pygame.RESIZABLE)
        pygame.display.set_caption("Snake Game")
        self.blue_rect = Rect(width//2, height//2, Display.SQUARE_PIX, Display.SQUARE_PIX)
        pygame.draw.rect(self.dis, Display.BLUE, self.blue_rect)
        pygame.display.update()
        red_l,red_t = self.rand_red_location()
        self.red_rect = Rect(red_l, red_t, Display.SQUARE_PIX, Display.SQUARE_PIX)
        pygame.draw.rect(self.dis, Display.RED, self.red_rect)
        pygame.display.update()
        self.fps_millis = 5

    def rand_red_location(self) -> tuple[int,int]:
        """Returns a valid random location for the red rectangle to spawn.

        Returns:
            tuple[int,int]: x,y coordinates of the top left part of the rectangle.
        """        
        valid_loc = False
        red_l = 0
        red_t = 0
        while not valid_loc:
            red_l = random.randint(0, self.width-Display.SQUARE_PIX)
            red_t = random.randint(0, self.height-Display.SQUARE_PIX)
            dirs = [[0,0], [Display.SQUARE_PIX,0], [Display.SQUARE_PIX, Display.SQUARE_PIX], [0, Display.SQUARE_PIX]]
            # all dims of red square
            valid_loc = True
            for dir in dirs:
                x = red_l + dir[0]
                y = red_t + dir[1]
                print(self.dis.get_at((x,y)))
                if x < 0 or x > self.width or y < 0 or y > self.height or self.dis.get_at((x,y)) == pygame.Color(Display.BLUE):
                    valid_loc = False
                    break
            print(x,y)
        return (red_l,red_t)
    
    def game_loop(self):
        moved = False
        clk = Clock()
        game_over = False
        prev_move = (0,0)
        while not game_over:
            clk.tick(self.fps_millis)
            for event in pygame.event.get():
                print(event)
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    x,y = (0,0)
                    delta = 10
                    if event.key == pygame.K_LEFT:
                        x = -delta
                    elif event.key == pygame.K_RIGHT:
                        x = delta
                    elif event.key == pygame.K_DOWN:
                        y = delta
                    elif event.key == pygame.K_UP:
                        y = -delta
                    self.blue_rect.move_ip(x,y)
                    prev_move = (x,y)
                    moved = True
                else:
                    moved = False
            if not moved:
                print(prev_move)
                self.blue_rect.move_ip(prev_move[0], prev_move[1])
            self.dis.fill(Display.BLACK)
            pygame.draw.rect(self.dis, Display.RED, self.red_rect)
            pygame.draw.rect(self.dis, Display.BLUE, self.blue_rect)
            pygame.display.update()
            if self.blue_rect.left < 0 or self.blue_rect.right > self.width or self.blue_rect.top < 0 or self.blue_rect.bottom > self.height:
                game_over = True
        print("Goodbye")
        pygame.quit()
        quit()

if __name__ == "__main__":
    disp = Display(600, 300)
    disp.game_loop()
