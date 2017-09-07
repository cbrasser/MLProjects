import pygame
import numpy as np




display_width = 1250
display_height = 750
car_height = 20
car_width = 44
#X, Y and Angle in rad (0 = faced straight right)
initial_car_pos = [40,550,0]
initial_speed = 1
black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
green = (0,255,0)
red = (255,0,0)
angles = [-0.785, -0.392,0,0.392,0.785]
half_diag = np.sqrt(car_width*car_width + car_height*car_height)/2



clock = pygame.time.Clock()

pygame.init()
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Cars')
level_img = pygame.image.load('level_test.png')
car_img = pygame.image.load('car.png')
circle_img = pygame.image.load('circle.png')


gameDisplay.blit(level_img, (0,-1100))



def level():
    gameDisplay.blit(level_img, (0,-1100))
def car(x,y,angles, car_img_new):
    center = car_img_new.get_rect().center
    x_center = car_img_new.get_rect().move(x,y).centerx
    y_center = car_img_new.get_rect().move(x,y).centery
    left = car_img_new.get_rect().move(x,y).left
    top = car_img_new.get_rect().move(x,y).top
    right = car_img_new.get_rect().move(x,y).right
    bottom = car_img_new.get_rect().move(x,y).bottom
    width = car_img_new.get_rect().move(x,y).width
    height = car_img_new.get_rect().move(x,y).height
    gameDisplay.blit(car_img_new, (x,y))
    pygame.draw.rect(gameDisplay, green,(x,y,3,3))
    #Degrees, positive x is 0, -y is negative, y is positive
    direction = 0
    sensors = []
    for angle in angles:
        sensor = [0,0]
        sensor[0]= x_center+ np.cos(angle)*60
        sensor[1] = y_center +np.sin(angle)*60
        sensors.append(sensor)
    angle = angles[2]
    hitpoints=[]

    angle = angles[2]*180/np.pi
    per = np.absolute((angle) / 90)
    hitpoint1 = [0,0]
    hitpoint1[0] = left + (1-per)*width % width
    hitpoint1[1] = top

    hitpoint2 = [0,0]
    hitpoint2[0] = left + width
    hitpoint2[1] = top + (1-per)*height % height

    hitpoint3 = [0,0]
    hitpoint3[0] = left
    hitpoint3[1] = bottom -(1-per)*height % height

    hitpoint4 = [0,0]
    hitpoint4[0] = left + per*width % width
    hitpoint4[1] = bottom
    #hitpoint[0] = x_center + np.cos(1.4*angle)*car_width/2
        #hitpoint[1] = top
    hitpoints.append(hitpoint1)
    hitpoints.append(hitpoint2)
    hitpoints.append(hitpoint3)
    hitpoints.append(hitpoint4)

    pygame.draw.rect(gameDisplay, red, car_img_new.get_rect().move(x,y),1)
    pygame.draw.rect(gameDisplay, red, [hitpoints[0][0],hitpoints[0][1],5,5])
    pygame.draw.rect(gameDisplay, red, [hitpoints[1][0],hitpoints[1][1],5,5])
    pygame.draw.rect(gameDisplay, red, [hitpoints[2][0],hitpoints[2][1],5,5])
    pygame.draw.rect(gameDisplay, red, [hitpoints[3][0],hitpoints[3][1],5,5])
    for sensor in sensors:
        pygame.draw.rect(gameDisplay, green, [sensor[0],sensor[1],2,2])
    return hitpoints





def collision_points(hitpoints):
    '''
    *---------*
    |         |
    *---------*
    '''
    # Front left: 0°: upper right, 90°: upper left, 180°: lower left, 270°: lower right
    # 0-90:
    for hp in hitpoints:

        test =tuple(level_img.get_at((int(hp[0]),int(hp[1]))))
        print(test)
        if test[0] <= 5 and test[1]<=5 and test[2]<=5:

            return True

        return False



def accelerate(speed):
    if speed + 0.1*speed < 10:
        return speed + 0.1*speed
    else:
        return 10

def deccelerate(speed):
    if speed - 0.1*speed > 1:
        return speed - 0.1*speed
    else:
        return 1

def turn(curr_direction,dir_to_turn, turn_intensity):
    return curr_direction + turn_intensity*dir_to_turn

def race():
    turning_left = False
    turning_right = False
    global car_img
    turning_intensity = 0.1
    car_img_new = car_img
    x = initial_car_pos[0]
    y = initial_car_pos[1]
    angle = initial_car_pos[2]
    rt_angles = [i+initial_car_pos[2] for i in angles]
    print(rt_angles)
    speed = initial_speed

    exit = False
    accelerating = False
    while not exit:

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    accelerating=True
                if event.key == pygame.K_LEFT:
                    turning_left = True
                if event.key == pygame.K_RIGHT:
                    turning_right = True
                if event.key == pygame.K_DOWN:
                    exit = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    accelerating = False
                if event.key == pygame.K_LEFT:
                    turning_left = False
                if event.key == pygame.K_RIGHT:
                    turning_right = False
        if turning_left:
            #Angle before this frame
            tmp_angle = rt_angles[2]*180 / np.pi
            print('tmp_angle: ',tmp_angle)
            #Angle to rotate
            delta_angle = 180*turning_intensity/np.pi
            print('delta: ',delta_angle)
            #Rotate the original picture for the angle before the frame + the new part
            car_img_new = pygame.transform.rotozoom(car_img,-(tmp_angle - delta_angle),1)
            #Update the angles
            rt_angles = [turn(angle,-1, turning_intensity) for angle in rt_angles]
        elif turning_right:
            tmp_angle = rt_angles[2]*180 / np.pi
            delta_angle = 180*turning_intensity/np.pi
            car_img_new = pygame.transform.rotozoom(car_img,-(tmp_angle + delta_angle),1)
            rt_angles = [turn(angle,1, turning_intensity) for angle in rt_angles]
        if accelerating:
            speed = accelerate(speed)
        else:
            speed = deccelerate(speed)
        gameDisplay.fill(white)
        level()
        x = x+ np.cos(rt_angles[2])*speed
        y = y + np.sin(rt_angles[2])*speed
        hp =[]
        hp =car(x,y,rt_angles, car_img_new)
        # if collision_points(hp):
        #     exit = True
        #circle(int(x),int(y),rt_angles)
        pygame.draw.rect(gameDisplay, green,(x,y,3,3))
        pygame.draw.rect(gameDisplay, red,(x,y,3,3))

        pygame.display.update()


        clock.tick(60)
if __name__ == "__main__":

    race()
