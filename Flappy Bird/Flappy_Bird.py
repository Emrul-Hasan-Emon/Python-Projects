import pygame
from pygame.locals import *
import random

pygame.init()

# Timer for moving the ground image
clock = pygame.time.Clock()
fps = 50 

screen_width = 850
screen_height = 680

# define font
font = pygame.font.SysFont('Bauhaus 93', 60)

#define color
white = (255, 255, 255)

# Game window 
screen = pygame.display.set_mode((screen_width, screen_height)) #Blank Game Window
#Title
pygame.display.set_caption("Flappy Game")

# define game variables
ground_scroll = 0
scroll_speed = 3
flying = False # Initially the bird will not move
game_over = False
pipe_gap = 230
pipe_frequency = 1500 # 1.5 seconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False

# background image
bg = pygame.image.load('img/bg1.png')
ground_img = pygame.image.load('img/ground.png')
button_img = pygame.image.load('img/restart.png')

"""
    For showing the score on the window there is no functional way. The thing we have to do is
    covert the score into image and then by blit function we can show the score on window
"""

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color) # Convert the txt into an image
    screen.blit(img, (x, y))
    
# Reset the game
def reset_game():
    pipe_group.empty() # Delete everything from pipe group
    # Give the position of the bird to its initial position
    flappy.rect.x = 100
    flappy.rect.y = 500
    score = 0 # Reset the score to zero 
    return score

class Bird(pygame.sprite.Sprite):
    def __init__ (self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = [] # Empty list which will contain the images of all movement of the bird
        self.index = 0
        self.counter = 0 # Controls the speed of the animation
        
        for num in range(1, 4):
            img = pygame.image.load(f'img/bird{num}.png')
            self.images.append(img)
            
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.velocity = 0
        self.clicked = False
        
    def update(self): # This function is for animation
        
        if flying == True:
            # Gravity which takes bird downward
            self.velocity += 0.3
            if self.velocity > 8: 
                self.velocity = 8
            if self.rect.y < 680: 
                self.rect.y += int(self.velocity)
        
        if game_over == False:
            # jump
            if pygame.mouse.get_pressed()[0] == 1:
                self.velocity -= 1
                
            # handle animation
            self.counter += 1
            flap_cooldown = 5
            
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1 # Which bird image will be shown will be declared by index variable
                if self.index >= len(self.images): 
                    self.index = 0
            self.image = self.images[self.index]
            
            # rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.velocity * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


class Pipe(pygame.sprite.Sprite):
    def __init__ (self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        
        # Position 1 is from the top and -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        else:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]
            
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()


class Button():
    def __init__ (self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
    def draw(self):
        action = False
        
        # Get mouse position
        pos = pygame.mouse.get_pos()
        
        # Check if mouse is over button for that we have to check collision between the mouse position and the image
        if self.rect.collidepoint(pos): # Confirm the mouse cursor is on the restart image
            if pygame.mouse.get_pressed()[0] == 1: # Whether the mouse cursor clicked with left one on the image or not
                action = True
                
        # Draw Button
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action

bird_group = pygame.sprite.Group() # It is almost like pthon list
flappy = Bird(100, 500) # Created an instance of Bird class. This is bird which will be shown on window 
bird_group.add(flappy) # bird_group keeps the track of bird

pipe_group = pygame.sprite.Group() # It is also like python list

# Instance of Button class
button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)

run = True
#Game Loop
while run:
    clock.tick(fps)

    # Show image in the window. To show anything in window we use blit function of pygame module
    screen.blit(bg, (ground_scroll, 0))
    
    # Check the score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        
        if pass_pipe == True and bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
            pass_pipe = False
            score += 1
    # Draw the gorund  -> screen.blit(ground_img, (ground_scroll, 550))
    
    # Look for collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0: # Check whether the bird has crossed the border or not
        game_over = True
        
    # groupcollide function is used to check collision between two groups
    
    # Check if the bird has hit the ground
    if flappy.rect.bottom > 680 :
        game_over = True
        flying = False
    
    bird_group.draw(screen) # Display the bird
    bird_group.update()
    pipe_group.draw(screen) # Display the pipe
    
    if game_over == False and flying == True:
        # Generate new pipe
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            bottom_pipe = Pipe(screen_width, 400 + pipe_height, -1)
            top_pipe = Pipe(screen_width, 400 + pipe_height, 1)
            pipe_group.add(bottom_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now
            
        # Draw and scroll the nackground image
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35: 
            ground_scroll = 0
        pipe_group.update() # Pipe will be updated when only the game is running
    
    draw_text(str(score), font, white, int(screen_width / 2), 20)
    
    # Check for game over and reset
    if game_over == True:
        if button.draw() == True:
            game_over = False
            score = reset_game()
            
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # It is for cross sign on the right top corner for exiting the window
            run = False # The program will not execute
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True # Now the bird will start moving
            
    pygame.display.update() # Without this function nothing will appear in window
            
pygame.quit()