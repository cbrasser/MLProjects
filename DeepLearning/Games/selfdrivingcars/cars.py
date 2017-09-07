import pygame
import numpy as np

display_width = 1250
display_height = 750

black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
green = (0,255,0)
angles = [-0.785, -0.392,0,0.392,0.785]

clock = pygame.time.Clock()

#copterImg = pygame.image.load('copter.png')

pygame.init()
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Cars')
level_img = pygame.image.load('level_test.png')
gameDisplay.blit(level_img, (0,-1100))

def level():
    gameDisplay.blit(level_img, (0,-1100))
def car(x,y):
    #gameDisplay.blit(carImg, (x,y))
    pygame.draw.rect(gameDisplay, blue, [x,y, 44, 20])
    #Degrees, positive x is 0, -y is negative, y is positive
    direction = 0
    sensors = []
    for angle in angles:
        sensor = [0,0]
        sensor[0]= x+22+ np.cos(angle)*40
        sensor[1] = y+10 +np.sin(angle)*40
        sensors.append(sensor)

    for sensor in sensors:
        pygame.draw.rect(gameDisplay, green, [sensor[0],sensor[1],5,5])


def draw(thingx, thingy, thingw, thingh):
    #pygame.draw.rect(gameDisplay, blue, [thingx, thingy, thingw, thingh])
    pygame.draw.rect(gameDisplay, black, [thingx, thingy, thingw, thingh],1)


def create_track():

    walls =[
    [5,0,5,700],
    [60,0,5,140],
    [100,50,5,650],
    [140,50,5,650]
    ]
    return walls

def draw_walls():
    walls = create_track()
    for wall in walls:
        draw(wall[0],wall[1],wall[2],wall[3])




exit = False
while not exit:

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                exit = True

    gameDisplay.fill(white)
    level()
    #draw_walls()
    car(20, 550)
    pygame.display.update()

    clock.tick(60)
