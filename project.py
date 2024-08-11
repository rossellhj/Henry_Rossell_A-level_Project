print("Welcome")

import pygame
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 150, 255)

##with open("highscores/highscores.txt","r") as highscores:
##    for line in highscores:
##        print(line)

 
pygame.init()
 
WIDTH=700
HEIGHT=500
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("")

done = False
state="Main Menu"
health=100
#player = pygame.image.load('player.png')
playerx=200
playery=200
left=False
right=False

level=0

box_pos=0

house=""

lowest_time=99.9


firing_timer=0
timer=0
finish_time=0
enemy_fire=True



class SelectBox(pygame.sprite.Sprite):
    def __init__(self, width, height, alpha=100):
        super().__init__()

        
        #create box with transparency
        self.image=pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, alpha))
        self.rect=self.image.get_rect()

    def move(self, posx, posy):
        self.rect.x=posx
        self.rect.y=posy





class Block(pygame.sprite.Sprite):
 
    def __init__(self, color, width, height):
 
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

        

class Line(pygame.sprite.Sprite):
    def __init__(self, color, start_pos, end_pos, width=1):
        super().__init__()
        # initialise line class attributes
        self.color = color
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.width = width
        # create surface and rect for line - so can be added to all_sprites_list
        
    def update(self):
        self.image = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.line(self.image, self.color, self.start_pos, self.end_pos, self.width)
        self.rect = self.image.get_rect()

    def updateLine(self, startpos, endpos):
        self.start_pos=startpos
        self.end_pos=endpos
        self.update()


        


    def intersects_platform(self, start_pos, end_pos, platforms): #checks if line of sight intersects a platform

        #create bounding rectangle to check for intersections;
        #top left corner is min x and y co-ords, width and height are differences in start_pos/end_pos x and y co-ords
        line_rect = pygame.Rect(min(start_pos[0], end_pos[0]), min(start_pos[1], end_pos[1]),
                                abs(start_pos[0] - end_pos[0]), abs(start_pos[1] - end_pos[1]))
        
        for platform in platforms: #check if line clips any platform
            if platform.rect.clipline(start_pos, end_pos):
                return True
        return False

        


class Bullet(pygame.sprite.Sprite):
    def __init__(self, color, start_pos, end_pos, radius, speed):
        super().__init__()
        # initialise line class attributes
        self.color = color
        self.pos=start_pos
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.radius = radius
        self.speed = speed
        self.direction = self.calculateDirection()
        # create surface and rect for circle - so can be added to all_sprites_list
        
    
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)  #use a smaller surface for the bullet
        pygame.draw.circle(self.image, self.color, (radius, radius), radius)
        self.rect = self.image.get_rect(center=start_pos)

    def update(self):
        self.pos = (self.pos[0] + self.direction[0] * self.speed, self.pos[1] + self.direction[1] * self.speed)
        self.rect.center = self.pos   

    def updateCircle(self, pos):
        self.pos=pos
        self.update()

    def calculateDirection(self):

        #calculate x and y components of distance between enemy + player
        dx = self.end_pos[0] - self.start_pos[0]
        dy = self.end_pos[1] - self.start_pos[1]

        #use Pythagoras theorem to calculate magnitude of distance between enemy + player
        distance = math.sqrt(dx ** 2 + dy ** 2)  
        if distance == 0: #do not allow bullets fired when player + enemy occupying same position
            return (0, 0)
        else:
            return (dx / distance, dy / distance) #return unit vector by dividing vector by magnitude









        

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


class Enemy(ImageBlock):
    def __init__(self, image_path, width, height):
        super().__init__(image_path, width, height)

##    def tempLine(self):
##        self.temp_shoot=Line(BLACK, (self.rect.x, self.rect.y), (player.rect.x,player.rect.y))
##        all_sprites_list.add(self.temp_shoot)
##
##    def updateLine():
##        pass
##        
        

        

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

    def sword(self):
        # instantiate temporary box where sword is being struck
        self.temp_hit = Block(WHITE,50,50)
        self.temp_hit.rect.x=self.rect.x
        self.temp_hit.rect.y=self.rect.y
        all_sprites_list.add(self.temp_hit)

        # check for collision with enemy

        
        if self.temp_hit.rect.colliderect(enemy1.rect):
            return True
        
        return False

    def remove_sword(self):
        self.temp_hit.kill()



        

line1 = Line(RED, (100, 100), (500, 100))



#bullet1 = Bullet(BLACK, (100,100),(400,200), 4, 10)




platforms = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
menu_box = pygame.sprite.Group()

select_box=SelectBox(200,75) # instantiate the selecting box

menu_box.add(select_box)


player=Player("player.png", 25, 50) # instantiate the player
player.rect.x=50
player.rect.y=50

enemy1=Enemy("enemy.png", 25, 50) # instantiate the enemy
enemy1.rect.x=400
enemy1.rect.y=50
enemies.add(enemy1)

finish=ImageBlock("finish.png",127/4,458/4)
finish.rect.x=(700-(127/4))
finish.rect.y=(300-(458/4))


block1=Block(BLACK,200,200)
block1.rect.x=0
block1.rect.y=300
block2=Block(BLACK,300,300)
block2.rect.x=400
block2.rect.y=300
block3=Block(BLACK,100,15)
block3.rect.x=400
block3.rect.y=100


line2 = Line(BLACK, (enemy1.rect.x, enemy1.rect.y), (player.rect.x,player.rect.y))



bullet = Bullet(BLACK, enemy1.rect.center, player.rect.center, 5, 10)



platforms.add(block1, block2, block3)
all_sprites_list.add(player, block1, block2, block3, finish, enemy1, line1)







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
                    if box_pos==0:
                        state = "Select team"
                    else:
                        state="Highscores"
                elif state == "Select team":
                    state = "Select level"
                elif state == "Select level":
                    state = "Level 1"
            if event.key == pygame.K_UP:
                player.rect.y-=20
                box_pos-=1
            elif event.key == pygame.K_DOWN:
                player.rect.y+=20
                box_pos+=1
            elif event.key == pygame.K_LEFT:
                left=True
            elif event.key == pygame.K_RIGHT:
                right=True
            elif event.key == pygame.K_SPACE:
                player.jump()
            elif event.key == pygame.K_f:
                
                if player.sword():
                    print("killed")
                    enemies.remove(enemy1)
                    enemy1.kill()
                    enemy_fire=False
            
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left=False
            if event.key == pygame.K_RIGHT:
                right=False
            if event.key == pygame.K_f:
                player.remove_sword()

    screen.fill(BLUE)

    if state == "Main Menu":
        text(40, "Main Menu", 240, 50)
        text(25, "Select Team", 275, 200)
        text(25, "Highscores", 280, 270)

        menu_box.update()
        menu_box.draw(screen)

        if box_pos<0: # ensure select box positions have a range
            box_pos=0
        elif box_pos>1:
            box_pos=1

        if box_pos==0:
            select_box.rect.x=250
            select_box.rect.y=175
        elif box_pos==1:
            select_box.rect.y=250


    if state == "Highscores":
        text(40, "Highscores", 240, 50)

        
        
    if state == "Select team":
        text(40, "Select Team", 240, 50)
        text(20, "Drake", 320, 160)
        text(20, "Grenville", 300, 200)
        text(20, "Howard", 310, 240)
        text(20, "Jonson", 310, 280)
        text(20, "Marlowe", 305, 320)
        text(20, "Raleigh", 305, 360)
        text(20, "Sidney", 310, 400)
        text(20, "Spenser", 305, 440)

        menu_box.update()
        menu_box.draw(screen)
        

        if box_pos<0: # ensure select box positions have a range
            box_pos=0
        elif box_pos>7:
            box_pos=7

        if box_pos==0:
            select_box.rect.x=250
            select_box.rect.y=140
            select_box.rect.height=10
            house="Drake"
        elif box_pos==1:
            select_box.rect.y=180
            house="Grenville"
        elif box_pos==2:
            select_box.rect.y=220
            house="Howard"
        elif box_pos==3:
            select_box.rect.y=260
            house="Jonson"
        elif box_pos==4:
            select_box.rect.y=300
            house="Marlowe"
        elif box_pos==5:
            select_box.rect.y=340
            house="Raleigh"
        elif box_pos==6:
            select_box.rect.y=380
            house="Sidney"
        elif box_pos==7:
            select_box.rect.y=420
            house="Spenser"


            
            

    if state == "Select level":
        text(40, "Select Level", 240, 50)
        text(40, "1", 150, 150)
        menu_box.update()
        menu_box.draw(screen)

        select_box.rect.x=100
        select_box.rect.y=120

    if state == "Level 1":
        

        
        level=1
        timer+=1
        time=timer/60 #convert number of frames to seconds
        
        text(15, "Health:", 20, 10)
        text(15, str(health), 100,10)
        text(15, "Timer:", 575, 10)
        text(15, str(round(time, 2)), 635, 10)
        #screen.blit(player, (playerx,playery))
        all_sprites_list.add(player)

        
##        platforms.add(block1, block2, block3)
##        all_sprites_list.add(block1, block2, block3, finish, enemy1)

        
        
        


        if left:   #handling of movement with variables to ensure key holds
            player.rect.x-=4
        if right:
            player.rect.x+=4

            

        if player.rect.colliderect(finish.rect): #check for collision with finish line
            print(house) # works
            
            directory="highscores/{0}.txt".format(house) # define location of highscores text file

            finish_time=round(time, 2)

            

            with open(directory, "r") as times: # fetch lowest time for particular team
                lines=times.readlines()
                print(lines)
                
                lowest_time=lines[0].strip() # removes \n characters

            

            if float(lowest_time)<finish_time:
                print("not beaten")
            else:
                print("beaten")
                lines[0]="{0}\n".format(str(finish_time)) # ensure new line break for easy retrieval of times
                
                with open(directory, 'w') as highscores:
                    highscores.writelines(lines)

                

                
            state="Finish"

        if player.rect.y>550: #reset player if they fall off screen
            print("fallen")
            player.rect.x=50
            player.rect.y=50


        if firing_timer % 60 == 0: #every 60 frames/1.0 seconds create bullet object
            if enemy_fire: #will be False if enemy has been killed
                bullet = Bullet(BLACK, (enemy1.rect.x, enemy1.rect.y), (player.rect.x, player.rect.y), 5, 1)
                bullets.add(bullet)
                all_sprites_list.add(bullet) #separate sprite group for bullets



        for bullet in bullets:
            bullet.update()
            if bullet.rect.colliderect(player.rect): #check for bullet collision with player for each bullet
                print("Hit!")
                health -= 25
                bullet.kill() #remove bullet after it has hit the player
            if bullet.rect.x > 700 or bullet.rect.x < 0 or bullet.rect.y > 500 or bullet.rect.y < 0:
                bullet.kill()
                print("removed bullet")


        if health<=0:
            state = "Fail" #go to "level failed" screen

            

        #line1.updateLine((enemy1.rect.x + 5,enemy1.rect.y + 25), (player.rect.x + 12.5, player.rect.y + 10))
        
        enemy_pos = (enemy1.rect.x + 5, enemy1.rect.y + 25)
        player_pos = (player.rect.x + 12.5, player.rect.y + 10)
        if line1.intersects_platform(enemy_pos, player_pos, platforms): #check for line intersection using method
            enemy_fire=False #stop enemy fire when this occurs
        elif not(line1.intersects_platform(enemy_pos, player_pos, platforms)) and len(enemies)!=0: #check for NOT line intersection using method and enemy existence
            enemy_fire=True #continue enemy fire when this occurs

        line1.updateLine(enemy_pos, player_pos)
        
     

        #bullet1.updateCircle((player.rect.x, player.rect.y))


        #bullet.update()
        
        

        all_sprites_list.draw(screen)


        
        


        

        player.update(platforms)

        

    if state == "Finish":
        text(40, "Level {0} Complete".format(level), 170, 50)
        text(25, "Time: {0}".format(str(finish_time)), 275, 200)
        text(20, "Main Menu", 100, 400)
        text(20, "Restart", 310, 400)
        text(20, "Level Select", 475, 400)



        
        with open(directory, "r") as times:
            lines=times.readlines()
            lowest_time=lines[level-1].strip() # removes \n characters

        text(20, "Quickest Time: {0}".format(str(lowest_time)), 225, 275)

    
        
        menu_box.update()
        menu_box.draw(screen)

        if box_pos==0: # set select box positions on screen
            select_box.rect.x = 60  
            select_box.rect.y = 375
        elif box_pos==1:
            select_box.rect.x=270
        elif box_pos==2:
            select_box.rect.x=460

        if box_pos<0: # ensure select box positions have a range
            box_pos=0
        elif box_pos>2:
            box_pos=2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    
                    #reset values for restart
                    
                    time=0
                    timer=0
                    finish_time=0
                    player.rect.x=50
                    player.rect.y=50
                    for bullet in bullets:
                        bullets.remove(bullet)
                        bullet.kill()
                    health=100
                    left=False
                    right=False
                    enemy1=Enemy("enemy.png", 25, 50) # re-instantiate the enemy
                    enemy1.rect.x=400
                    enemy1.rect.y=50
                    enemies.add(enemy1)
                    all_sprites_list.add(enemy1)


                    if box_pos==1: # menu option handling
                        state = "Level 1"
                    if box_pos==0:
                        state = "Main Menu"
                    if box_pos==2:
                        state = "Select level"

                    box_pos=0 # reset select box position for next time
                    
                elif event.key == pygame.K_LEFT:
                    box_pos-=1
                elif event.key == pygame.K_RIGHT:
                    box_pos+=1

               
            
                    


    if state == "Fail":
        text(40, "Level failed", 200, 50)

        
    
        

    
        
    pygame.display.flip()

    firing_timer+=1

    clock.tick(60)

pygame.quit()

highscores.close()
