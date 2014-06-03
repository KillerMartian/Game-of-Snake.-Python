# Kyler Martin: Game of Snake
# started 1-22-14
# Make sure you have access to Pygame.

# Imports everything that I need
import pygame, sys
from pygame.locals import *
import random

class Game(object):
    """
    Class called Game that contain all the attributes and methods that interact 
    with the game board. Encapsulation - Grouping data and operations because 
    within game there are methods and attributes.
    """
    # Colors
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    GREEN = (0, 225, 0)    
    
    def __init__(this, width, height):
        """
        The __init__ assigns variables to the instance. Inheretance - Instances 
        vs. Class because the varriables are initiated to the instance not the 
        class.
        """
        
        # Board size
        this.Width = width # multiples of ten.
        this.Height = height # multiples of ten.
        
        #Clock settings
        this.fpsClock = pygame.time.Clock()
        this.score = 0
        
        # For stopping game
        this.playing = True
        #this.event = True
        
        # Window settings
        this.DISPLAYSURF = pygame.display.set_mode((this.Width + 1, this.Height + 1), 0, 32)
        pygame.display.set_caption('Game of Snake')
        
    def __str__(this):
        """
        Prints the size of the board and the score. Polymorphism - Operator
        overloading because the __ allows you to overload the method to print.
        """
        return "The boards size is %s by %s, and the current score is %s" % (this.Width, this.Height, this.score)
        
    def num_of_squares(this, length, num = 1, dev_by = 1): # Used in getting coordinates
        """
        Finds how many squares are in each row and gives you the ability to 
        find the middle if you set dev_by to 2
        """
        return ((num + (length / 10)) / dev_by)

    def check_for_hit(this, snake, walls, food):
        """
        Checks whether or not the head of the snake has just been drawn over 
        the food. If it has then the snake will grow, the score is incremented, 
        and a new food is placed on the board. If the snake did not hit food 
        then we see if the snake has hit itself or the walls. if it has then
        the snake stops moving and the main game loop is ended.
        """
        if snake.snake_pos[-1] == food.new_food_pos:
            snake.snake_new_len += snake.growth_rate
            this.score += 10
            food.find_rand_pos(this, snake)
            food.draw_food(this, this.RED, food.rand_food_pos)
        elif snake.snake_pos[-1] in snake.snake_pos[0:-2] or snake.snake_pos[-1] in walls.walls_pos:
            this.playing = False

    def grid_entire_board(this, board, color):
        """
        Fills the board with red squares that could be used for an end game
        screen. *currently not in use
        """
        for i in range(this.num_of_squares(this.Width)):
            for e in range(this.num_of_squares(this.Height)):
                seg = Segment(board, color, (i, e))
                
    def write(this, board, say, pos_x, pos_y):
        """
        Writes a message (say) on the screen (board) at the pos_x, pos_y
        """
        myfont = pygame.font.SysFont("monospace", 14)
        label = myfont.render(say, True, board.BLACK, board.WHITE)
        this.DISPLAYSURF.blit(label, (pos_x, pos_y)) 
        pygame.display.update()        
            
    def play_1_game(this, snake, walls, food):
        """
        The Main Game Loop. Writes the score in the top left corner of the 
        board, Moves the snake. Checks for a hit. ticks the clock and updates 
        the screen. Then checks for the last turn command or the quit game 
        button. The loop stops when a loosing hit happens then the score is 
        printed to the screen.
        """
        while this.playing == True: #  Main game loop
            this.write(this, str(this.score), 12,10)
            snake.move_snake(this)
            this.check_for_hit(snake, walls, food)
            
            this.fpsClock.tick(snake.speed)
            pygame.display.update()
            
            for event in pygame.event.get():
                this.event = event
                if this.event.type == pygame.KEYDOWN:
                    snake.change_direction(this)
                    pygame.display.update() 
                    break
                if this.event.type == QUIT:
                    pygame.quit()
                    sys.exit("Play Again!!!")
        this.write(this, "Your score is %s. To play again press space." % (this.score), 75,100)
                
    def __initialize(this, speed, growth, size_X, size_Y):
        """
        Initializes pygame, fills white, and then initializes the instances of 
        Game, Snake, Walls, and Food. Encapsulation - Information hiding because
        the instance initiolizing is hiden out of the main game loop.
        """
        pygame.init()
        this.G = Game(size_X, size_Y)
        this.G.DISPLAYSURF.fill(this.G.WHITE)
        this.S = Snake(this.G, speed, growth)
        this.W = Walls(this.G)
        this.F = Food(this.G)        
    
    def Play(this, speed, growth, size_X, size_Y):
        """
        Starts the game then allows you to restart the game when you lose by
        pressing space and looping again.
        """
        while True:
            this.__initialize(speed, growth, size_X, size_Y)
            this.G.play_1_game(this.S, this.W, this.F)
            play = False
            while play == False:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            play = True
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()            

class Segment(object):
    """
    The Class Segment the holds all the methods and attributes that are
    responsible for drawing segments. Encapsulation - Grouping data and 
    opperations because there are methods and attributes. - Interface vs. 
    Implementation because the implementation for the drawing is within Segment
    and the interface is in the other classes.
    """
    
    def __init__(this, board, color, (x, y)):
        """
        """
        this.draw_square(board, color, (x,y))
        
    def coordinates(this, x, y):
        """
        Indexes to the pixle that is on the upper left hand corner of each 
        square. returns the coordinates of the pixel in a list.
        """
        new_x = 1 + (x-1) * 10
        new_y = 1 + (y-1) * 10
        return [new_x, new_y]
        
    def draw_square(this, board, color, (x, y,)):
        """
        Uses pygames draw.rect function to draw a rectangle on the board. First
        calls the method coordinates to find what pixel the top left corner of 
        the square should be on.
        """
        cords_list = this.coordinates(x, y)
        new_x = cords_list[0]
        new_y = cords_list[1]
        pygame.draw.rect(board.DISPLAYSURF, color, (new_x, new_y, 9, 9))   

class Snake(Game):
    """
    The Class Snake the holds all the methods and attributes that interact with
    the snake. Encapsulation - Grouping data and opperations because there
    are methods and attributes. Inheretance - Sharing Structure because 
    Snake uses the methods from game that draw on the board.
    """
    
    def __init__(this, board, speed, growth_rate):
        """
        The __init__ assigns variables to the instance. Inheretance - Instances 
        vs. Class because the varriables are initiated to the instance not the 
        class.
        """
        this.speed = speed
        this.growth_rate = growth_rate
        this.facing_X = "0" # can be +, 0, or -
        this.facing_Y = "+"# can be +, 0, or -
        this.snake_start_pos = [(2, 2), (2, 3), (2, 4), (2, 5), (2, 6)]
        this.snake_pos = this.snake_start_pos[:]
        this.snake_len = len(this.snake_pos)
        this.snake_new_len = this.snake_len
        for i in range(len(this.snake_start_pos)): # Puts a Green snake on the board starting in the left corner
            seg = Segment(board, board.GREEN, this.snake_start_pos[i])
        
    def __str__(this):
        """
        Prints the size of the snake, the direction its facing, its speed, and 
        its growth rate. Polymorphism - Operator overloading because the __ 
        allows you to overload the method to print.
        """
        return "This snake's position is %s, its X and Y directoins are %s, %s, its speed is %s, and its growth rate is %s" % (this.snake_start_pos, this.facing_X, this.facing_Y, this.speed, this.growth_rate)


    def move_snake(this, board):
        """
        Moves the snake in the direction that it is facing either + or - in the 
        X or Y direction. Makes the snake grow if its length is shorter that the
        new_length.
        """
        old_head = this.snake_pos[-1]

        if this.snake_len >= this.snake_new_len:
            seg = Segment(board, this.WHITE, this.snake_pos[0])
            del this.snake_pos[0]
            
        if this.facing_X == "+":
            new_head = (old_head[0] + 1, old_head[1])
        elif this.facing_X == "-":
            new_head = (old_head[0] - 1, old_head[1])
            
        if this.facing_Y == "+":
            new_head = (old_head[0], old_head[1] + 1)
        elif this.facing_Y == "-":
            new_head = (old_head[0], old_head[1] - 1)
            
        this.snake_len = len(this.snake_pos)
        this.snake_pos.append(new_head)
        seg = Segment(board, this.GREEN, this.snake_pos[-1])


    def change_direction(this, board):
        """
        Checks to see what arrow key was pressed then changes the direction of
        the snake. It must be used inside of a pygame event loop.
        """
        if this.facing_Y == "+" or this.facing_Y == "-":
            if board.event.key == pygame.K_LEFT:
                this.facing_X = "-"
                this.facing_Y = "0"
            elif board.event.key == pygame.K_RIGHT:
                this.facing_X = "+"
                this.facing_Y = "0"
                
        elif this.facing_X == "+" or this.facing_X == "-":
            if board.event.key == pygame.K_UP:
                this.facing_Y = "-"
                this.facing_X = "0"
            elif board.event.key == pygame.K_DOWN:
                this.facing_Y = "+"
                this.facing_X = "0"

class Walls(Game):
    """
    The Class Snake the holds all the methods and attributes that interact with
    the snake. Encapsulation - Grouping data and opperations because there
    are methods and attributes. Inheretance - Sharing Structure because 
    Walls uses the methods from game.
    """
    
    def __init__(this, board):
        """
        Initializes the walls positions arround the outside of the board then
        draws them.
        """
        walls_left_pos = [(1, y) for y in range(board.num_of_squares(board.Height))]
        walls_top_pos = [(x, 1) for x in range(board.num_of_squares(board.Width))]
        walls_bottom_pos = [(x, board.num_of_squares(board.Height, 0)) for x in range(board.num_of_squares(board.Width))]
        walls_right_pos = [(board.num_of_squares(board.Width, 0), y) for y in range(board.num_of_squares(board.Width))]
        
        this.walls_pos = walls_left_pos + walls_top_pos + walls_bottom_pos + walls_right_pos   
        
        this.draw_walls(board)
        
    def draw_walls(this, board):
        """
        Draws all of the walls arround the outside of the board.
        """
        
        for i in range(board.num_of_squares(board.Width)):
            seg = Segment(board, board.BLACK, (i,1))
            seg = Segment(board, board.BLACK, (i,board.num_of_squares(board.Height, 0)))
        for i in range(board.num_of_squares(board.Height)):
            seg = Segment(board, board.BLACK, (1,i))
            seg = Segment(board, board.BLACK, (board.num_of_squares(board.Height, 0),i))

class Food(Game):
    """
    The Class Food the holds all the methods and attributes that interact with
    the food. Encapsulation - Grouping data and opperations because there
    are methods and attributes. Inheretance - Sharing Structure because 
    food uses the methods from game.
    """
    
    def __init__(this, board):
        """
        Initiates the food position and drawing it on the board.
        """
        this.start_food_pos = (board.num_of_squares(board.Width, 0, 2), (board.num_of_squares(board.Height, 0, 2)))
        this.new_food_pos = this.start_food_pos[:]
        this.draw_food(board, board.RED, this.new_food_pos)
        
    def __str__(this):
        """
        Prints the foods current position. Operator overloading because 
        the __ allows you to overload the method to print.
        """
        return "The food is %s at" % (str(this.new_food_pos))
    
    def draw_food(this, board, color, pos):
        """
        Draws the food at on the board at pos.
        """
        seg = Segment(board, color, pos)
        
    def find_rand_pos(this, board, snake):
        """
        Looks for a random position for the food, on the board, that is not 
        in the snake or the walls
        """
        this.rand_food_pos = (random.randint(2, ((board.Width/10)-1)), random.randint(2, ((board.Height/10)-1)))
        while this.rand_food_pos in snake.snake_pos:    
            this.rand_food_pos = (random.randint(2, ((board.Width/10)-1)), random.randint(2, ((board.Height/10)-1)))
        this.new_food_pos = this.rand_food_pos        
 

game = Game(0,0) # Just so I can call Play on and instance.
speed = 20
growth_rate = 5
size_x = 500
size_y = 500
game.Play(speed, growth_rate, size_x, size_y)
# High Score 380