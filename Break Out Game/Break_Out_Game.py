import pygame
import pygame.locals

# Creating Game Window
pygame.init()

# Size of the window
screen_width = 696
screen_height = 696

screen = pygame.display.set_mode((screen_width, screen_height))  # Creating scree window
pygame.display.set_caption("Breakout")  # Title of the window

# Define Colors
background_color = (234, 218, 184)  # Background Color -> Gray

# Block Colors
block_red = (242, 85, 96)  # Red blocks
block_green = (86, 174, 87)  # Green blocks
block_blue = (69, 177, 232)  # Blue bloks
block_orange = (255, 165, 0)  # Orange blocks

# Paddle Colors
paddle_color = (142, 135, 123)
paddle_outline = (100, 100, 100)

# Define font style
font = pygame.font.SysFont('Constantia', 90)
font2 = pygame.font.SysFont('Constantia', 30)

# Define text color
text_color = (0, 0, 0) # Black
text_color2 = (78, 81, 139)

# Define game variables. rows are numbered from top to bottom and cols are numbered from left to right
rows = 8
cols = 8
clock = pygame.time.Clock()
fps = 50
live_ball = False
game_over = 0

# Convert text to image
def draw_text(text, font, text_color, x, y):
    # Covert the text into image
    image = font.render(text, True, text_color)
    # Then show the image in window
    screen.blit(image, (x, y))
    return image

class check_image():
    def __init__ (self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
    def draw(self):
        action = False
        
        # Get mouse position
        pos = pygame.mouse.get_pos()
        
        # Check if mouse is over button for that we have to check collision between the mouse position and the image
        if self.rect.collidepoint(pos): # Confirm the mouse cursor is on the start image or close image
            if pygame.mouse.get_pressed()[0] == 1: # Whether the mouse cursor clicked with left one on the image or not
                action = True
                
        return action

# Brick wall class
class Wall():  # For block
    def __init__(self):
        # Define block height and weight
        self.width = screen_width // cols
        self.height = 50  # 50 pixel

    def create_wall(self):
        self.blocks = []  # Contains all blocks 2D grid and 2 column for each row. first column contain the information
        # of the block and second column contain the strength of the block
        block_individual = []  # contains details of each individual block

        # Create total rowsxcols = 8x8 = 64 blocks
        for row in range(rows):
            # Reset the block row list
            block_row = []  # Contains all blocks information which will be in this row
            # Iterate through each of the column
            for col in range(cols):
                # As each block will be a rectangle they have co-ordinate x and y
                # Generate x and y position for each block and create a rectangle from
                block_x = col * self.width  # position x will be increasing
                block_y = row * self.height

                # Now create a rectangle with left top corner x and y
                rect = pygame.Rect(block_x, block_y, self.width, self.height)

                # Assign block strength for each of the row
                if row < 2:
                    strength = 4
                elif row < 4:
                    strength = 3
                elif row < 6:
                    strength = 2
                else:
                    strength = 1

                # Store the block into the a list
                block_individual = [rect, strength]
                # Append this individual block into block_row list
                block_row.append(block_individual)

            # Job of each indivial row is done and now store this row details
            self.blocks.append(block_row)

    def draw_wall(self):
        for row in self.blocks:
            for block in row:
                # Assign color based on strength
                if (block[1] == 4):
                    block_color = block_orange
                elif (block[1] == 3):
                    block_color = block_blue
                elif (block[1] == 2):
                    block_color = block_green
                else:
                    block_color = block_red

                # Show the block into the window
                pygame.draw.rect(screen, block_color, block[0])
                # Draw border for each of the block
                pygame.draw.rect(screen, background_color, block[0], 2)  # 2=Thickness of the border


# Paddle class
class Paddle():
    def __init__(self):
        self.reset()

    def move(self):
        # Reset movement direction. Direction will be left or right.
        self.direction = 0

        # Get the key which is pressed
        key = pygame.key.get_pressed()

        # Move the paddle in left side
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        # Move the paddle in the right side
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed
            self.direction = 1

    def draw(self):
        pygame.draw.rect(screen, paddle_color, self.rect)
        pygame.draw.rect(screen, paddle_outline, self.rect, 3)  # 3 = thickness of the border

    def reset(self):
        # Define paddle height and weight
        self.height = 20  # 20pixel
        self.width = screen_width // cols

        # Co-ordinate of left top corner of the paddle
        self.x = int((screen_width / 2) - (self.width / 2))
        self.y = screen_height - (self.height * 2)
        self.speed = 10  # Paddle moving speed
        # Now create a pabble of rectangle with left most corner co-ordinate
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direction = 0  # Direction in which paddle is moving


class Ball():
    def __init__(self, x, y):
        self.reset(x, y)

    @property
    def move(self):
        # Collision threshold
        collision_thresh = 5

        # assume that every block is broken
        wall_broken = 1

        # Now check collision between the ball and block. if collision occurs reduce the strength of the block if
        # strength is larger than 1 otherwise remove the block
        row_count = 0  # For iterating on rows
        for row in wall.blocks:  # Access field of Wall class using instance of Wall class wall
            item_count = 0
            for item in row:
                # Check if the collision between wall and ball occurs
                if self.rect.colliderect(item[0]):  # First index is the information of rectangle of block
                    # Check if collision was from above of the block and bottom of the ball
                    if abs(self.rect.bottom - item[0].top) < collision_thresh and self.speed_at_y > 0:
                        self.speed_at_y *= -1  # Ball will start moving upward
                    # Check if collision was from bottom of the block and top of the ball
                    if abs(self.rect.top - item[0].bottom) < collision_thresh and self.speed_at_y < 0:
                        self.speed_at_y *= -1  # Ball will start moving downward
                    # Check if collision was from left side of the block and right side of the ball
                    if abs(self.rect.right - item[0].left) < collision_thresh and self.speed_at_x > 0:
                        self.speed_at_x *= -1  # Ball will start moving left side
                    # Check is collision was from right side of the block and left side of the ball
                    if abs(self.rect.left - item[0].right) < collision_thresh and self.speed_at_x < 0:
                        self.speed_at_x *= -1  # Ball will start moving right side

                    # reduce the block strength if the strength is greater than 1 otherwise disappear the block
                    if wall.blocks[row_count][item_count][1] > 1:
                        wall.blocks[row_count][item_count][1] -= 1
                    else:
                        wall.blocks[row_count][item_count][0] = (
                            0, 0, 0, 0)  # We cannot delete the block because it will
                        # change the order of the block we can make the block null

                # check if any of the block's strength is greater than zero because that mean every block is not destroyed
                if wall.blocks[row_count][item_count][0] != (0, 0, 0, 0):
                    wall_broken = 0
                # increase item count
                item_count += 1
            # increase row count
            row_count += 1

        # after iterating through all blocks check all block is broken or not
        # if wall_broken = 1 it means all wall is broken
        if wall_broken == 1:
            self.game_over = 1  # It means player manages to break all the block and won
        # Check for collision with the wall left and right side
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed_at_x *= -1

        # Check for collision with the wall top and bottom
        if self.rect.top < 0:  # if ball touches the top wall then it will start coming to the bottom
            self.speed_at_y *= -1
        if self.rect.bottom > screen_height:  # if ball touches the fround the game is over
            self.game_over = -1  # It means the ball go down beyond the paddle and the player lost

        # Look for collision with paddle
        if self.rect.colliderect(player_paddle):
            # check if colliding with top
            if abs(self.rect.bottom - player_paddle.rect.top) < collision_thresh and self.speed_at_y > 0:
                self.speed_at_y *= -1
                self.speed_at_x += player_paddle.direction
                if self.speed_at_x > self.speed_max:
                    self.speed_at_x = self.speed_max
                elif self.speed_at_x < 0 and self.speed_at_x < -self.speed_max:
                    self.speed_at_x = -self.speed_max
            else:
                self.speed_at_x *= -1
                """
                if the ball touches the left side of the paddle then the ball moves to left and if the ball 
                touches the right side of the paddle then it moves to right side and speed of y will not change
                It means the ball will go down as previous
                """

        self.rect.x += self.speed_at_x
        self.rect.y += self.speed_at_y

        return self.game_over

    def draw(self):
        # Draw the circle over the paddle
        pygame.draw.circle(screen, paddle_color, (self.rect.x + self.ball_radius, self.rect.y + self.ball_radius),
                           self.ball_radius)
        pygame.draw.circle(screen, paddle_outline, (self.rect.x + self.ball_radius, self.rect.y + self.ball_radius),
                           self.ball_radius, 3)

    def reset(self, x, y):
        # Define Ball position
        self.ball_radius = 10
        self.x = x - self.ball_radius
        self.y = y

        # Take the space of the ball in a rectangular shape
        self.rect = pygame.Rect(self.x, self.y, self.ball_radius * 2, self.ball_radius * 2)
        self.speed_at_x = 4
        self.speed_at_y = -4
        self.speed_max = 5
        self.game_over = 0  # indicates whether the ball has touched the bottom line or not


# Instance of Wall class
wall = Wall()
wall.create_wall()

# Instance of Paddle class
player_paddle = Paddle()

# Instance of Ball class
ball = Ball(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)

# background image
background_image = pygame.image.load('back.png')

flag = False
run = True
while run:
    screen.blit(background_image, (0, 0))
    # Convert start text into image
    start_image = draw_text('Start', font, text_color, 265, 200)
    # Convert quit text into image
    close_image = draw_text('Quit', font, text_color, 265, 400)

    ch = check_image(265, 200, start_image)
    if ch.draw() == True:
        flag = True
        break
    ch = check_image(265, 400, start_image)
    if ch.draw() == True:
        break
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # It is for cross sign on the right top corner for exiting the window
            run = False
    pygame.display.update()  # This function update the game continuously
    
# Start the game
run = flag
while run:
    clock.tick(fps)  # The paddle will move now in a constant speed

    screen.fill(background_color)  # Fill the screen with the background color

    # Draw all objects
    wall.draw_wall()  # Draw wall and blocks
    player_paddle.draw()  # Draw the paddle in window
    ball.draw()  # Draw the ball

    if live_ball == True:
        player_paddle.move()  # Move the paddle
        game_over = ball.move  # Movement of the ball
        if game_over != 0:
            live_ball = False

    if live_ball == False:
        if game_over == 0:
            draw_text('CLICK ANYWHERE TO START', font2, text_color2, 145, 400)
        elif game_over == 1:
            draw_text('YOU WON!!', font2, text_color2, 260, 400)
            draw_text('CLICK ANYWHERE TO START', font2, text_color2, 145, 500)
        elif game_over == -1:
            draw_text('YOU LOST!!', font2, text_color2, 260, 400)
            draw_text('CLICK ANYWHERE TO START', font2, text_color2, 145, 500)
            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # It is for cross sign on the right top corner for exiting the window
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
            live_ball = True
            # Reset ball position. Means take the ball to its initial position
            ball.reset(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)
            # reset the paddle position. it means take the paddle to its initial position
            player_paddle.reset()
            # Reset wall. it doesn't require to reset the blocks because whenever create_wall is called blocks will be created automatically from the starting
            wall.create_wall()


    pygame.display.update()  # This function update the game continuously
pygame.quit()