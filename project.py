print("Welcome")

import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 150, 255)
 
pygame.init()
 
WIDTH=700
HEIGHT=500
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("")

done = False
state="Main Menu"
health=0
##player = pygame.image.load('player.png')
playerx=200
playery=200
left=False
right=False



class Block(pygame.sprite.Sprite):
    """
    This class represents the ball.
    It derives from the "Sprite" class in Pygame.
    """
 
    def __init__(self, color, width, height):
        """ Constructor. Pass in the color of the block,
        and its size. """
 
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        # Create an image of the block, and fill it with a color
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
 
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()

class ImageBlock(pygame.sprite.Sprite):
 
    def __init__(self, image_path, width, height):
 
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        # Load image from storage
        self.image = pygame.image.load(image_path).convert_alpha()
        # Scale image to desired width and height
        self.image=pygame.transform.scale(self.image, (width, height))
 
        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()

    def move_up(self):
        self.rect.y -= 20
    def move_down(self):
        self.rect.y += 20

class Player(ImageBlock):
    def __init__(self, image_path, width, height):
        super().__init__(image_path, width, height)
        self.velocity_y=0
        self.jump_height=-3

    def update(self, platforms):
        self.velocity_y+=0.3
        self.rect.y+=self.velocity_y

        # check for collisions with platforms
        collisions = pygame.sprite.spritecollide(self, platforms, False)
        for platform in collisions:
            # if the player is moving downwards, stop downwards movement
            if self.velocity_y >0:
                self.rect.bottom = platform.rect.top
                self.velocity_y=0

    def jump(self):
        self.velocity_y=self.jump_height
        


platforms = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

player=Player("player.png", 25, 50) # instantiate the player
player.rect.x=50
player.rect.y=50


block1=Block(BLACK,200,200)
block1.rect.x=0
block1.rect.y=300
block2=Block(BLACK,300,300)
block2.rect.x=400
block2.rect.y=300
block3=Block(BLACK,100,15)
block3.rect.x=400
block3.rect.y=100









def text(size, text, posx, posy):   #for quicker text blitting
    font = pygame.font.SysFont('courier', size, True, False)
    text = font.render((text),True,BLACK)
    screen.blit(text, [posx, posy])

clock = pygame.time.Clock()

while not done:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Handle state transitions
                if state == "Main Menu":
                    state = "Select team"
                elif state == "Select team":
                    state = "Select level"
                elif state == "Select level":
                    state = "Level 1"
            if event.key == pygame.K_UP:
                player.rect.y-=20
            elif event.key == pygame.K_DOWN:
                player.rect.y+=20
            elif event.key == pygame.K_LEFT:
                left=True
            elif event.key == pygame.K_RIGHT:
                right=True
            elif event.key == pygame.K_SPACE:
                player.jump()
            
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left=False
            if event.key == pygame.K_RIGHT:
                right=False
            
    screen.fill(BLUE)

    if state == "Main Menu":
        text(40, "Main Menu", 240, 50)
        text(25, "Select Team", 275, 200)
        text(25, "Highscores", 280, 250)
        
    if state == "Select team":
        text(40, "Select Team", 240, 50)
        text(20, "Drake", 290, 200)
        text(20, "Grenville", 260, 240)

    if state == "Select level":
        text(40, "Select Level", 240, 50)

    if state == "Level 1":
        
        text(15, "Health:", 20, 10)
        text(15, str(health), 100,10)
        text(15, "Timer:", 600, 10)
        #screen.blit(player, (playerx,playery))
        all_sprites_list.add(player)

        
        platforms.add(block1, block2, block3)
        all_sprites_list.add(block1, block2, block3)

        player.update(platforms)
        all_sprites_list.draw(screen)




        if left:   # Handling of movement with variables to ensure key holds
            player.rect.x-=3
        if right:
            player.rect.x+=3

        


    
        
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
