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

done=False
pause=False
state="Main Menu"
health=100
#player = pygame.image.load('player.png')
playerx=200
playery=200
left=False
right=False

player_speed=5
double_speed_activated=False
double_speed_timer=0

player_jump_height=-7.5
high_jump_activated=False
high_jump_timer=0

level=0
temp_level=0



spawnx=0
spawny=0

box_pos=0

house=""
houses=["Drake", "Grenville", "Howard", "Jonson", "Marlowe", "Raleigh", "Sidney", "Spenser"]
house_initials=["D:", "G:", "H:", "J:", "M:", "R:", "Si:", "Sp:"]

lowest_time=99.9


firing_timer=0
bullet_speed=0
bullet_freq=0
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
        alpha=(*self.color[:3],0) # add transparency
        pygame.draw.line(self.image, alpha, self.start_pos, self.end_pos, self.width) 
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


class PowerUp(ImageBlock):
    def __init__(self, image_path, width, height):
        super().__init__(image_path, width, height)




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
        self.jump_height=player_jump_height
        self.velocity_x=0
        self.gravity = .3

    def update(self, platforms):
        # Horizontal movement and collision
        self.rect.x += self.velocity_x
        collisions = pygame.sprite.spritecollide(self, platforms, False)
        for platform in collisions:
            if self.velocity_x > 0:  #moving right
                self.rect.right = platform.rect.left
            elif self.velocity_x < 0:  #moving left
                self.rect.left = platform.rect.right

        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        #self.on_ground = False
        collisions = pygame.sprite.spritecollide(self, platforms, False)
          #reset ground check
        for platform in collisions:
            #self._on_ground = False
            if self.velocity_y > 0:  #when falling
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.on_ground = True
            elif self.velocity_y < 0:  #when jumping
                self.rect.top = platform.rect.bottom
                self.velocity_y = 0
                self.on_ground = True
            else:
                self.on_ground = False

        if self.velocity_y == 0 and not self.on_ground:
            self.rect.y += 1


    def setJumpHeight(self, player_jump_height):
        self.jump_height=player_jump_height
    
    def jump(self): 
        self.velocity_y = self.jump_height

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

select_box=SelectBox(200,50) # instantiate the selecting box
#select_box.rect.height=10

menu_box.add(select_box)

background1=ImageBlock("background1.png",1000,1000) # instantiate the background
background2=ImageBlock("background2.png",1000,1000) 

player=Player("player.png", 25, 50) # instantiate the player
player.rect.x=spawnx
player.rect.y=spawny

enemy1=Enemy("enemy.png", 25, 50) # instantiate the enemy
enemy1.rect.x=400
enemy1.rect.y=50
enemies.add(enemy1)

double_speed=PowerUp("double_speed.png", 25, 25) # instantiate the double speed power up
double_speed.rect.x=1000
double_speed.rect.y=1000

high_jump=PowerUp("high_jump.png", 25, 25)
high_jump.rect.x=1000
high_jump.rect.y=1000






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
block4=Block(BLACK,300,15)
block4.rect.x=1000
block4.rect.y=1000
block5=Block(BLACK,50,15)
block5.rect.x=390
block5.rect.y=300
block6=Block(BLACK,50,50)
block6.rect.x=1000
block7=Block(BLACK,50,150)
block7.rect.x=1000
block8=Block(BLACK,50,250)
block8.rect.x=1000


line2 = Line(BLACK, (enemy1.rect.x, enemy1.rect.y), (player.rect.x,player.rect.y))



bullet = Bullet(BLACK, enemy1.rect.center, player.rect.center, 5, bullet_speed)



platforms.add(block1, block2, block3, block4, block5, block6, block7, block8)
all_sprites_list.add(background1, player, block1, block2, block3, block4, block5,
                     block6, block7, block8, finish, enemy1, line1, double_speed,
                     high_jump)








def text(size, text, posx, posy):   #for quicker text blitting
    font = pygame.font.SysFont('courier', size, True, False)
    text = font.render((text),True,BLACK)
    screen.blit(text, [posx, posy])

clock = pygame.time.Clock()

while not done:

    if not pause:
    
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
                        # Go to different level states based on position of select box
                        if box_pos==0:
                            state = "Level 1"
                        elif box_pos==1:
                            state = "Level 2"
                        elif box_pos==2:
                            state = "Level 3"
                        else:
                            state = "Level 4"
                    elif state == "Highscores":
                        state = "Main Menu"
                if event.key == pygame.K_UP:
                    player.rect.y-=20
                    box_pos-=1
                elif event.key == pygame.K_DOWN:
                    player.rect.y+=20
                    box_pos+=1
                elif event.key == pygame.K_LEFT:
                    left=True
                    box_pos-=1
                elif event.key == pygame.K_RIGHT:
                    right=True
                    box_pos+=1
                elif event.key == pygame.K_SPACE:
                    if player.velocity_y <= 0.3 and player.velocity_y >= -0.3: #check if player is vertically stationary
                        player.jump()
                elif event.key == pygame.K_ESCAPE:
                    pause=True
                    
                        
                    
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
                select_box.rect.y=190
            elif box_pos==1:
                select_box.rect.y=260


        if state == "Highscores":
            text(40, "Highscores", 240, 25)

            text(40, "1", 125, 75)
            text(40, "2", 275, 75)
            text(40, "3", 425, 75)
            text(40, "4", 575, 75)

            initial_height=132.5

            for house_initial in house_initials:
                text(30, house_initial, 15, initial_height)
                initial_height+=40

            

            
            width=110

            for level in range(4):
                height=135 # reset height variable for each level
                for house in houses: 
                    with open("highscores/{0}.txt".format(house), "r") as times: # fetch lowest time for each team
                        lines=times.readlines()
                        text(25, lines[level].strip(), width, height) # remove special newline characters
                        height+=40
                width+=150
                        


            

            
            
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
            
            select_box.rect.height=10
            menu_box.update()
            menu_box.draw(screen)
            

            if box_pos<0: # ensure select box positions have a range
                box_pos=0
            elif box_pos>7:
                box_pos=7

            if box_pos==0:
                select_box.rect.x=250
                select_box.rect.y=145
                select_box.rect.height=10
                house="Drake"
            elif box_pos==1:
                select_box.rect.y=185
                house="Grenville"
            elif box_pos==2:
                select_box.rect.y=225
                house="Howard"
            elif box_pos==3:
                select_box.rect.y=265
                house="Jonson"
            elif box_pos==4:
                select_box.rect.y=305
                house="Marlowe"
            elif box_pos==5:
                select_box.rect.y=345
                house="Raleigh"
            elif box_pos==6:
                select_box.rect.y=385
                house="Sidney"
            elif box_pos==7:
                select_box.rect.y=425
                house="Spenser"


                
                

        if state == "Select level":
            text(40, "Select Level", 240, 100)
            text(40, "1", 125, 250)
            text(40, "2", 275, 250)
            text(40, "3", 425, 250)
            text(40, "4", 575, 250)
            
            menu_box.update()
            menu_box.draw(screen)

            if box_pos==0:
                select_box.rect.x=25
                select_box.rect.y=250
            elif box_pos==1:
                select_box.rect.x=175
            elif box_pos==2:
                select_box.rect.x=325
            elif box_pos==3:
                select_box.rect.x=475

            if box_pos<0:
                box_pos=0
            elif box_pos>3:
                box_pos=3



        if state == "Level 1" or state == "Level 2" or state == "Level 3" or state == "Level 4":

            



            


            

            for block in platforms: # moving all objects off screen before defining layouts
                block.rect.x=1000

            for enemy in enemies:
                enemy.rect.x=1000


            if state == "Level 1":
                
                if level!=1:
                    
                    
                    level=1
                    spawnx=50
                    spawny=50
                    player.rect.x=spawnx # only set player's position once not every frame
                    player.rect.y=spawny
                    bullet_speed=1
                    bullet_freq=60
                    
                    

                block1.rect.x=0
                block1.rect.y=300
                block2.rect.x=400
                block2.rect.y=300
                block3.rect.x=400
                block3.rect.y=100
                block4.rect.x=1000
                block4.rect.y=1000
                block5.rect.x=1000
                block5.rect.x=1000
                block6.rect.x=1000
                block7.rect.x=1000

                enemy1.rect.x=400
                enemy1.rect.y=50

                finish.rect.x=(700-(127/4))
                finish.rect.y=(300-(458/4))
                
                
            if state == "Level 2":
                if level!=2:                
                    spawnx=100
                    spawny=350
                    player.rect.x=spawnx
                    player.rect.y=spawny
                    bullet_speed=3
                    bullet_freq=30
                    #double_speed=PowerUp("double_speed.png", 25, 25)
                    double_speed.rect.x=650
                    double_speed.rect.y=342.5
                    level=2

                block1.rect.x=100 
                block1.rect.y=450
                block2.rect.x=450
                block2.rect.y=380
                block3.rect.x=400
                block3.rect.y=100
                block4.rect.x=0
                block4.rect.y=240
                block5.rect.x=390
                block5.rect.y=300
                finish.rect.x=0
                finish.rect.y=125

                enemy1.rect.x=400
                enemy1.rect.y=50



                
            if state == "Level 3":
                if level!=3:                
                    spawnx=100
                    spawny=350
                    player.rect.x=spawnx
                    player.rect.y=spawny
                    bullet_speed=1
                    bullet_freq=60
                    block6.rect.x=200
                    block6.rect.y=300
                    high_jump.rect.x=550
                    high_jump.rect.y=312.5
                    level=3
                    

                block1.rect.x=-150
                block1.rect.y=225
                block2.rect.x=300
                block2.rect.y=350
                block5.rect.x=100 
                block5.rect.y=450
                block4.rect.x=450
                block4.rect.y=100
                
                block6.rect.x=200
                #block.rect.y=400



                if (timer%1)==0: #run every frame
                    if (timer%(300))<150:
                        block6.rect.y+=1 #change positions of block for moving
                    else:
                        block6.rect.y-=1
                

                enemy1.rect.x=450


                finish.rect.y=0
                finish.rect.x=668

            if state == "Level 4":
                if level!=4:
                    high_jump_timer=0
                    spawnx=550
                    spawny=350
                    player.rect.x=spawnx
                    player.rect.y=spawny
                    bullet_speed=1
                    bullet_freq=60
                    high_jump.rect.x=610
                    high_jump.rect.y=412.5
                    level=4

                block1.rect.x=1000

                block2.rect.x=1000

                block3.rect.x=1000

                block4.rect.x=2000
                block4.rect.y=450

                block5.rect.x=600
                block5.rect.y=450

                block6.rect.x=500
                block6.rect.y=400

                block7.rect.x=350
                block7.rect.y=300

                block8.rect.x=200
                block8.rect.y=200

                finish.rect.x=0
                finish.rect.y=100

                enemy1.rect.x=100








            if player.rect.y>550: #reset player if they fall off screen
                print("fallen")
                player.rect.x=spawnx
                player.rect.y=spawny


            if firing_timer % bullet_freq == 0: #every 60 frames/1.0 seconds create bullet object
                if enemy_fire: #will be False if enemy has been killed
                    bullet = Bullet(BLACK, (enemy1.rect.x, enemy1.rect.y), (player.rect.x, player.rect.y), 5, bullet_speed)
                    bullets.add(bullet)  #separate sprite group for bullets
                    all_sprites_list.add(bullet)



            for bullet in bullets:
                bullet.update()
                if bullet.rect.colliderect(player.rect): #check for bullet collision with player for each bullet
                    print("Hit!")
                    health -= 25
                    bullet.kill() #remove bullet after it has hit the player
                if bullet.rect.x > 700 or bullet.rect.x < 0 or bullet.rect.y > 500 or bullet.rect.y < 0:
                    bullet.kill()
                    print("removed bullet")
                    

            if double_speed.rect.colliderect(player.rect): #check for player collision with double speed power up
                double_speed_activated=True
                player_speed=7.5 #change speed
                double_speed.kill() #remove power up
                

            if high_jump.rect.colliderect(player.rect): #check for player collision with high jump power up
                high_jump_activated=True
                if level!=3:
                    player.setJumpHeight(-10.0) #change jump height
                elif level==3:
                    player.setJumpHeight(-13.0)
                high_jump.kill() #remove power up



         

            if health<=0:
                state = "Fail" #go to "level failed" screen

            enemy_pos = (enemy1.rect.x + 5, enemy1.rect.y + 25)
            player_pos = (player.rect.x + 12.5, player.rect.y + 10)
            if line1.intersects_platform(enemy_pos, player_pos, platforms): #check for line intersection using method
                enemy_fire=False #stop enemy fire when this occurs
            elif not(line1.intersects_platform(enemy_pos, player_pos, platforms)) and len(enemies)!=0: #check for NOT line intersection using method and enemy existence
                enemy_fire=True #continue enemy fire when this occurs

            line1.updateLine(enemy_pos, player_pos)
       

            all_sprites_list.draw(screen)


            

            player.update(platforms)

            collisions = pygame.sprite.spritecollide(player, platforms, False)
            if collisions and player.velocity_y >= 0:  # Player is touching a platform
                can_jump = True
            else:
                can_jump = False


        


            

            timer+=1
            time=timer/60 #convert number of frames to seconds


            if (timer%4)==0: #run every 4 frames
                if (timer%(120))<60:
                    double_speed.rect.y+=1 #change positions of power ups for bobbing
                    high_jump.rect.y+=1
                else:
                    double_speed.rect.y-=1
                    high_jump.rect.y-=1
                
                
            if double_speed_activated:
                double_speed_timer+=1 #increment timer

            if double_speed_timer>=150: #reset after 2.5 seconds
                double_speed_activated=False
                double_speed_timer=0
                player_speed=5

            if high_jump_activated:
                high_jump_timer+=1 #increment timer

            if high_jump_timer>=180 and level!=3: #reset after 3.0 seconds
                high_jump_activated=False
                high_jump_timer=0
                player.setJumpHeight(-7.5)

            if high_jump_timer>=210 and level==3: #reset after 5.0 seconds
                high_jump_activated=False
                high_jump_timer=0
                player.setJumpHeight(-7.5)

            
            text(15, "Health:", 20, 10)
            text(15, str(health), 100,10)

            if double_speed_activated and (double_speed_timer%30)<=20: #check if double speed is activated
                text(15, "DOUBLE SPEED", 275, 10)

            if high_jump_activated and (high_jump_timer%30)<=20: #check if high jump is activated
                text(15, "HIGH JUMP", 300, 10)
            
            text(15, "Timer:", 575, 10)
            text(15, str(round(time, 2)), 635, 10)
            all_sprites_list.add(player)

            if left:   #handling of movement with variables to ensure key holds
                player.velocity_x=-player_speed
            elif right:
                player.velocity_x=player_speed
            else:
                player.velocity_x=0

                

            if player.rect.colliderect(finish.rect): #check for collision with finish line
                print(house) # works
                
                directory="highscores/{0}.txt".format(house) # define location of highscores text file

                finish_time=round(time, 2)

                #player.setJumpHeight(-7.5)

                box_pos=0

                

                with open(directory, "r") as times: # fetch lowest time for particular team
                    lines=times.readlines()
                    print(lines)
                    
                    lowest_time=lines[level-1].strip() # removes \n characters

                

                if float(lowest_time)<finish_time:
                    print("not beaten")
                else:
                    print("beaten")
                    lines[level-1]="{0}\n".format(str(finish_time)) # ensure new line break for easy retrieval of times
                    
                    with open(directory, 'w') as highscores:
                        highscores.writelines(lines)

                #level=0

                
                    
                state="Finish"


        if state == "Level 2":
            pass

        if state == "Level 3":
            pass

        if state == "Level 4":
            pass

            

        if state == "Finish" or state == "Fail":

            if state == "Finish":
                text(40, "Level {0} Complete".format(level), 170, 50)
                text(25, "Time: {0}".format(str(finish_time)), 275, 200)
            text(20, "Main Menu", 100, 400)
            text(20, "Restart", 310, 400)
            text(20, "Level Select", 475, 400)

            
            if state == "Fail":
                text(40, "Level failed", 200, 50)

           
            if state == "Finish":
                with open(directory, "r") as times:
                    lines=times.readlines()
                    lowest_time=lines[level-1].strip() # removes \n characters

                text(20, "Quickest Time: {0}".format(str(lowest_time)), 225, 275)

        
            
            menu_box.update()
            menu_box.draw(screen)

            if box_pos==0: # set select box positions on screen
                select_box.rect.x = 60  
                select_box.rect.y = 388
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
                        player_speed=5
                        player.rect.x=spawnx
                        player.rect.y=spawny
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
                        double_speed_activated=False
                        double_speed_timer=0
                        double_speed=PowerUp("double_speed.png", 25, 25)
                        double_speed.rect.x=1000
                        all_sprites_list.add(double_speed)
                        high_jump=PowerUp("high_jump.png", 25, 25)
                        high_jump.rect.x=1000
                        all_sprites_list.add(high_jump)
                        high_jump_activated=False
                        player.setJumpHeight(-7.5)


                        if box_pos==1: # menu option handling
                            temp_level=level
                            level=0 
                            state = "Level {0}".format(temp_level)
                        if box_pos==0:
                            level=0
                            state = "Main Menu"
                        if box_pos==2:
                            level=0
                            state = "Select level"

                        box_pos=0 # reset select box position for next time
                        
                    elif event.key == pygame.K_LEFT:
                        box_pos-=1
                    elif event.key == pygame.K_RIGHT:
                        box_pos+=1

                   
                
                        


        
            
        pygame.display.flip()

        firing_timer+=1
       

        clock.tick(60)

    elif pause: #pause screen
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done=True
                pause=False 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause=False  #unpause game
        
        #screen.fill(BLUE)

        all_sprites_list.draw(screen)

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA) #create surface over entire screen
        overlay.fill((0, 150, 255, 128)) #transparent fill
        screen.blit(overlay, (0, 0))
        


        text(40, "Paused", 300, 200)
        pygame.display.flip()

pygame.quit()

highscores.close()

