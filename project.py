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

def text(size, text, posx, posy):
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
                if state == "Main Menu":
                    state = "Select team"
                elif state == "Select team":
                    state = "Select level"
                elif state == "Select level":
                    state = "Level 1"
            
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
        
 
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
