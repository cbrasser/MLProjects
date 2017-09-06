import pygame
import time
import random
import numpy as np

#what if we train a model to fly the copter and then when he is really good we try to train a model to build walls to kill the copter ?

#---------------------Variables--------------------
main_score = 1
display_width = 800
display_height = 600
black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
green = (0,255,0)
free_space = display_height-340
copter_width = 73
wall_width= display_width/50
clock = pygame.time.Clock()
crashed = False
copterImg = pygame.image.load('copter.png')
direction = [0,0]
index =0

#----------------------Init------------------------
pygame.init()
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Copter')

def copter(x,y):
    gameDisplay.blit(copterImg, (x,y))

def draw(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])
    pygame.draw.rect(gameDisplay, black, [thingx, thingy, thingw, thingh],1)

def create_wall():
    prev_height_top = 0
    prev_x =-5
    prev_height_bottom = display_height-170
    upper_walls =[]
    lower_walls= []
    for i in range(0,55):
        upper_walls.append([-wall_width+i*wall_width,0,wall_width,170, green])
        lower_walls.append([-wall_width+i*wall_width,prev_height_bottom,wall_width,170,blue])
    return upper_walls, lower_walls

walls =create_wall()

def update_walls_without_drawing(score, copter_x,copter_y, index):

    #First number: 1 ->up, 0 -> down | Second number: #Frames we are already going in that direction
    global direction

    for wallGroup in walls:
        moved = False
        for counter in range(0,54):
            if not moved:
                moved = True
                index1 =0
                if index == 0:
                    index1=54
                else:
                    index1 = index-1

                wallGroup[index][0]=wallGroup[index1][0]

                if direction[0] == 1:

                    #Rate of going up dependent on how long we go in this direction

                    wallGroup[index][1]=wallGroup[index1][1] - (direction[1]+1)*2

                    #Deciding if we want to change direction dependent on how long we go into the prev direction
                    #REVIEW Might need to change the range
                    next_direction = random.randrange(0,10)
                    if next_direction <= direction[1] or (wallGroup[index][4]==green and wallGroup[index][1]<-150):
                        #print('CHANGING DIRECTION TO DOWN')
                        direction = [0,0]
                    direction[1]+= 1
                #Going down
                elif direction[0] == 0:
                    #print('we are going down')
                    #Rate of going down dependent on how long we go in this direction

                    wallGroup[index][1]=wallGroup[index1][1] + (direction[1]+1)*2
                    #Deciding if we want to change direction dependent on how long we go into the prev direction
                    #REVIEW Might need to change the 100
                    next_direction = random.randrange(0,10)
                    if next_direction <= direction[1] or (wallGroup[index][4]==blue and wallGroup[index][1]>display_height-20):
                        #print('CHANGING DIRECTION TO UP')
                        direction = [1,0]
                    direction[1]+= 1

            if not  counter == index:
                wallGroup[counter][0] -=wall_width

def update_walls(score, copter_x,copter_y, index):
    tempscore = score -1
    #First number: 1 ->up, 0 -> down | Second number: #Frames we are already going in that direction
    global direction

    for wallGroup in walls:
        moved = False
        for counter in range(0,54):
            if not moved:
                moved = True
                index1 =0
                if index == 0:
                    index1=54
                else:
                    index1 = index-1
                print(index, index1)
                wallGroup[index][0]=wallGroup[index1][0]

                if direction[0] == 1:

                    #Rate of going up dependent on how long we go in this direction

                    wallGroup[index][1]=wallGroup[index1][1] - (direction[1]+1)*2

                    #Deciding if we want to change direction dependent on how long we go into the prev direction
                    #REVIEW Might need to change the range
                    next_direction = random.randrange(0,10)
                    if next_direction <= direction[1] or (wallGroup[index][4]==green and wallGroup[index][1]<-150):
                        #print('CHANGING DIRECTION TO DOWN')
                        direction = [0,0]
                    direction[1]+= 1
                #Going down
                elif direction[0] == 0:
                    #print('we are going down')
                    #Rate of going down dependent on how long we go in this direction

                    wallGroup[index][1]=wallGroup[index1][1] + (direction[1]+1)*2
                    #Deciding if we want to change direction dependent on how long we go into the prev direction
                    #REVIEW Might need to change the 100
                    next_direction = random.randrange(0,10)
                    if next_direction <= direction[1] or (wallGroup[index][4]==blue and wallGroup[index][1]>display_height-20):
                        #print('CHANGING DIRECTION TO UP')
                        direction = [1,0]
                    direction[1]+= 1

            if not  counter == index:
                wallGroup[counter][0] -=wall_width

            if wallGroup[counter][1]>0 and wallGroup[counter][4] == green:
                draw(wallGroup[index][0],0,wallGroup[counter][2],wallGroup[counter][1]+30,green)
            elif wallGroup[counter][1]<display_height-170 and wallGroup[counter][4] == blue:
                draw(wallGroup[counter][0],wallGroup[counter][1]+160,wallGroup[counter][2],display_height-(wallGroup[counter][1]+170),blue)



            draw(wallGroup[counter][0],wallGroup[counter][1],wallGroup[counter][2],wallGroup[counter][3],wallGroup[counter][4])




            # if(wall[0]<-5):
            #     wall[0]=display_width
                #Going up


            # wall[0] -=wall_width


            #print(wall)

    return False

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',50)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)



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

def random_action2():
    return random.randrange(0,2)

def reset():
    global x
    global y
    global score
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
    walls =create_wall()

def crashCheck(copter_x,copter_y):
    for wallGroup in walls:
        index = 0
        for wall in wallGroup:
            if copter_x>=wall[0] and copter_x <= (wall[0]+wall[2]):
                if copter_y >= wall[1] and copter_y <= (wall[1]+wall[3]):
                    return True


def main_game_loop(action):

    global x
    global y
    global score
    global walls
    global index

    if action ==0:
         y+=5
    elif action == 1:
        y-=5

    score +=1

    update_walls_without_drawing(score,x,y,index)
    index +=1
    if index ==55:
        index =0
    done = crashCheck(x,y)
    #copter(x,y)
    delta_top = 0
    delta_bottom = 0
    top_bound =0
    bottom_bound =0
    for wall in walls[0]:
        if wall[0] > x-10 and wall[0] < x+10:
            delta_top=wall[1]+170
            top_bound =wall[1]+170
            break
    for wall in walls[1]:
        if wall[0] > x-10 and wall[0] < x+10:
            delta_bottom =wall[1]
            bottom_bound =wall[1]
            break
    # if np.absolute(delta_top - delta_bottom)/2 < (bottom_bound - top_bound)/4:
    #     score = 1
    # else:
    #     score = 0
    middle = bottom_bound - (bottom_bound - top_bound)/2
    if (y > middle and action == 0) or (y<middle and action ==1):
        score = 2
    else:
        score = -1

    #return np.array([x,y,delta_top,delta_bottom]), score, done
    return np.array([delta_top,delta_bottom]), score, done

def game_loop_testing(action):

    global x
    global y
    global score
    global gravity
    global vert_speed
    global hor_speed
    global timer
    global gravity_timer
    global up
    global exit
    global walls
    global index

    if action ==0:
         y+=5
    elif action == 1:
        y-=5
    gameDisplay.fill(white)
    score +=1
    display_score(score)

    update_walls(score,x,y, index)
    index +=1
    if index ==55:
        index =0
    done = crashCheck(x,y)
    copter(x,y)
    pygame.display.update()
    clock.tick(60)
    timer += 1
    gravity_timer +=1

    delta_top = 0
    delta_bottom = 0
    for wall in walls[0]:
        if wall[0] > x-10 and wall[0] < x+10:
            delta_top=wall[1]+170
            break
    for wall in walls[1]:
        if wall[0] > x-10 and wall[0] < x+10:
            delta_bottom =wall[1]
            break

    return np.array([delta_top,delta_bottom]), score, done

def main():
    index = 0
    x =  (display_width * 0.2)
    y = (display_height * 0.5)
    score = 0
    x_change = 0
    gravity = 1
    vert_speed =0
    hor_speed = 0
    timer = 0
    gravity_timer =0
    up = False
    walls =create_wall()
    exit = False
    #No boost



    #--------------------------------ONLY FOR HUMAN PLAYER
    while not exit:
        print(20*'_')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    exit = True
                elif event.key == pygame.K_SPACE:
                    #Go up
                    timer =0
                    up = True
                    #boost
                    action_chosen=1
                elif event.key == pygame.K_DOWN:
                    pygame.time.wait(10000)


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    up = False
                    timer = 0
                    gravity_timer = 0

        #x += x_change

        #-----------------HUMAN PLAYER
        if up:
            y += gravity - timer/2
        else:
            y += gravity +gravity_timer/5

        gameDisplay.fill(white)
        score +=1
        display_score(score)
        done = update_walls(score,x,y,index)

        index +=1
        if index ==55:
            index =0
        if crashCheck(x,y):
             quit()
        print('X: ',x)
        copter(x,y)

        pygame.display.update()
        clock.tick(60)
        timer += 1
        gravity_timer +=1



if __name__ == "__main__":
    main()

#main_game_loop()
# pygame.quit()
# quit()
