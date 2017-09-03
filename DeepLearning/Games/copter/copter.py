import pygame
import time
import random
import numpy as np


#what if we train a model to fly the copter and then when he is really good we try to train a model to build walls to kill the copter ?
main_score = 1

direction = [1,0]
pygame.init()


display_width = 800
display_height = 600

free_space = display_height-340

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Copter')



black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
green = (0,255,0)

copter_width = 73
wall_width= display_width/50
clock = pygame.time.Clock()
crashed = False
copterImg = pygame.image.load('copter.png')


def copter(x,y):
    gameDisplay.blit(copterImg, (x,y))

def things(thingx, thingy, thingw, thingh, color):




    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])


def create_walls_better():
    prev_height_top = 0
    prev_x =-5
    prev_height_bottom = display_height-170
    upper_walls =[]
    lower_walls= []
    for i in range(51):
        upper_walls.append([i*wall_width,0,20,170, green])
        lower_walls.append([i*wall_width,prev_height_bottom,20,170,blue])
    return upper_walls, lower_walls

walls =create_walls_better()

def update_walls(score, copter_x,copter_y):
    tempscore = score -1
    #First number: 1 ->up, 0 -> down | Second number: #Frames we are already going in that direction
    global direction

    for wallGroup in walls:
        index = 0
        for wall in wallGroup:
            if copter_x>=wall[0] and copter_x <= (wall[0]+wall[2]):
                if copter_y >= wall[1] and copter_y <= (wall[1]+wall[3]):
                    # crash()
                    return True
            if wall[1]>0 and wall[4] == green:
                things(wall[0],0,wall[2],wall[1]+30,green)
            elif wall[1]<display_height-170 and wall[4] == blue:
                things(wall[0],wall[1]+160,wall[2],display_height-(wall[1]+170),blue)

            if(wall[0]<-10):
                wall[0]=display_width
                #Going up

                if direction[0] == 1:

                    #Rate of going up dependent on how long we go in this direction
                    if index == 0:
                        index = 51
                    wall[1]=wallGroup[index-1][1] - (direction[1]+1)*2

                    #Deciding if we want to change direction dependent on how long we go into the prev direction
                    #REVIEW Might need to change the 100
                    next_direction = random.randrange(0,10)
                    if next_direction <= direction[1] or (wall[4]==green and wall[1]<-150):
                        #print('CHANGING DIRECTION TO DOWN')
                        direction = [0,0]
                    direction[1]+= 1
                #Going down
                elif direction[0] == 0:
                    #print('we are going down')
                    #Rate of going down dependent on how long we go in this direction
                    if index == 0:
                        index = 51
                    wall[1]=wallGroup[index-1][1] + (direction[1]+1)*2
                    #Deciding if we want to change direction dependent on how long we go into the prev direction
                    #REVIEW Might need to change the 100
                    next_direction = random.randrange(0,10)
                    if next_direction <= direction[1] or (wall[4]==blue and wall[1]>display_height-20):
                        #print('CHANGING DIRECTION TO UP')
                        direction = [1,0]
                    direction[1]+= 1
            wall[0] -=10
            things(wall[0],wall[1],wall[2],wall[3],wall[4])
            index +=1
            #print(wall)

    return False


def draw_walls(walls):

    for wallGroup in walls:
        for wall in wallGroup:
            things(wall[0],wall[1],wall[2],wall[3],wall[4])
            #print(wall)

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)

    game_loop()

def crash():
    message_display('You Crashed')

def display_score(score):

    font = pygame.font.SysFont(None, 25)
    text = font.render("Score: "+str(score), True, black)
    gameDisplay.blit(text,(20,200))


x =  (display_width * 0.2)
y = (display_height * 0.5)
score = 0
x_change = 1
gravity = 1
vert_speed =0
hor_speed = 0
timer = 0
gravity_timer =0
up = False

exit = False
def random_action(state):
    ran = random.randrange(0,10)
    #not pressed
    if state==0:
        #dont press
        if ran < 5:
            return 0
            #press
        else:
            return 1
    #pressed
    elif state == 1:
        #release
        if ran<5:
            return 2
        #keep pressed
        else:
            return 3

def reset():
    global x
    global y
    global score
    #global
    global gravity
    global vert_speed
    global hor_speed
    global timer
    global gravity_timer
    global up
    global exit
    global walls

    x =  (display_width * 0.2)
    y = (display_height * 0.5)
    score = 0
    x_change = 1
    gravity = 1
    vert_speed =0
    hor_speed = 0
    timer = 0
    gravity_timer =0
    up = False
    walls =create_walls_better()



def main_game_loop(action):

    global x
    global y
    global score
    #global
    global gravity
    global vert_speed
    global hor_speed
    global timer
    global gravity_timer
    global up
    global exit
    global walls
    #No boost
    action_chosen =0

    #while not exit:
    #print(20*'_')
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         crashed = True
    #
    #     if event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_UP:
    #             exit = True
    #         elif event.key == pygame.K_SPACE:
    #             #Go up
    #             timer =0
    #             up = True
    #             #boost
    #             action_chosen=1
    #
    #
    #     if event.type == pygame.KEYUP:
    #         if event.key == pygame.K_SPACE:
    #             up = False
    #             timer = 0
    #             gravity_timer = 0
    if action ==1:
         timer =0
         up = True
    elif action == 2:
        up = False
        timer = 0
        gravity_timer =0


    x += x_change
    if up:
        y += gravity - timer/2
    else:
        y += gravity +gravity_timer/5

    gameDisplay.fill(white)
    score +=1
    display_score(score)
    #draw_walls(walls)
    done = update_walls(score,x,y)


    copter(x,y)


    if x > display_width - copter_width or x < 0:
        gameExit = True

    #pygame.display.update()
    #clock.tick(60)
    timer += 1
    gravity_timer +=1
    # test = [[x],[y],walls[0],walls[1],[timer],[gravity_timer]]
    # test2 = np.concatenate([np.array(lis) for lis in test])
    return [x,y,timer,gravity_timer], score, done

class observation(object):
     def __init__(self):
        self.x = x
        self.y = y
        self.gravity = gravity
        #Maybe only give arrays with borders ?
        self.walls = walls
        self.timer = timer
        self.gravity_timer = gravity_timer

def setup():
    game = main_game_loop()

#main_game_loop()
# pygame.quit()
# quit()
