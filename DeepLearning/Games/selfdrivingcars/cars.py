import pygame
import numpy as np




display_width = 1250
display_height = 750
car_height = 20
car_width = 44
#X, Y and Angle in rad (0 = faced straight right)
initial_car_pos = [40,600,0]
initial_speed = 1
black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
green = (0,255,0)
red = (255,0,0)
angles = [-0.785, -0.392,0,0.392,0.785]
half_diag = np.sqrt(car_width*car_width + car_height*car_height)/2
#Originally 10, might be to fast for the pixel checks when crossing a road at close to 90°
#Didn't check how many pixels the was is thick at min.
max_speed = 7



clock = pygame.time.Clock()

pygame.init()
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Cars')
level_img = pygame.image.load('test_level_4.png')
car_img = pygame.image.load('car_test.bmp')
#circle_img = pygame.image.load('circle.png')


gameDisplay.blit(level_img, (0,0))



def level():
    gameDisplay.blit(level_img, (0,0))
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
    #pygame.draw.rect(gameDisplay, green,(x,y,3,3))
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

    angle = angles[2]*180/np.pi % 360


    per = (angle % 90)/90
    hitpoint1 = [0,0]
    hitpoint1[0] = right - (1-per)*width
    hitpoint1[1] = top

    hitpoint2 = [0,0]
    hitpoint2[0] = right
    hitpoint2[1] = bottom - (1-per)*height

    hitpoint3 = [0,0]
    hitpoint3[0] = left + (1-per)*width
    hitpoint3[1] = bottom

    hitpoint4 = [0,0]
    hitpoint4[0] = left
    hitpoint4[1] = top + (1-per)*height

    if angle <360 and angle >=270:
        hitpoints.append(hitpoint1)
        hitpoints.append(hitpoint2)
    elif angle <270 and angle >=180:
        hitpoints.append(hitpoint1)
        hitpoints.append(hitpoint4)
    elif (angle <180 and angle >=90):
        hitpoints.append(hitpoint3)
        hitpoints.append(hitpoint4)
    elif (angle <90 and angle >=0):
        hitpoints.append(hitpoint3)
        hitpoints.append(hitpoint2)


    for hp in hitpoints:
        pygame.draw.rect(gameDisplay, blue, [hp[0],hp[1],1,1])

    #pygame.draw.rect(gameDisplay, red, car_img_new.get_rect().move(x,y),1)

    for sensor in sensors:
        pygame.draw.rect(gameDisplay, green, [sensor[0],sensor[1],2,2])

    return hitpoints





def collision_check(hitpoints):
    '''
    check if the car drove into a wall by analysing the rgb color value at the 2 hitpoints in the front of the car
    the rear 2 hitpoints are currently not checked to increase performance
    '''
    tests= []

    for hp in hitpoints:

        tests.append(tuple(level_img.get_at((int(hp[0]+3),int(hp[1])))))
        tests.append(tuple(level_img.get_at((int(hp[0]-3),int(hp[1])))))
        tests.append(tuple(level_img.get_at((int(hp[0]),int(hp[1]+3)))))
        tests.append(tuple(level_img.get_at((int(hp[0]),int(hp[1]-3)))))
        #print(tuple(level_img.get_at((int(hp[0]+3),int(hp[1])))))

    for t in tests:

        if t[0] <= 5 and t[1]<=5 and t[2]<=5:
            return True
        return False

#TODO Write function to translate coordinates from the sensor from vector to polar form with magniute and angle
def read_sensors(sensors):
    '''
    Read the pixel color values in rgb format at the 5 sensors in front of the car
    Returns Color (currently or white/black as 0/1) and coordinates of point meassured

    '''
    colors_read = []
    for s in sensors:
        if tuple(level_img.get_at((int(s[0]),int(s[1])))) == (0,0,0,255):
            colors_read.append(1,s[0],s[1])
        else:
            colors_read.append(0,s[0],s[1])

    return colors_read


def accelerate(speed):
    if speed + 0.1*speed < max_speed:
        return speed + 0.1*speed
    else:
        return max_speed

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

            #Angle to rotate
            delta_angle = 180*turning_intensity/np.pi

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

        if collision_check(hp):
            exit = True
        # circle(int(x),int(y),rt_angles)

        #pygame.draw.rect(gameDisplay, green,(x,y,3,3))
        #pygame.draw.rect(gameDisplay, red,(x,y,3,3))

        pygame.display.update()


        clock.tick(60)
if __name__ == "__main__":

    race()
