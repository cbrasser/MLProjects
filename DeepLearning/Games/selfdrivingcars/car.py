import pygame
import numpy as np
import neural_network as nn

#------------------------display--------------
display_width = 1250
display_height = 750

#---------------------colors--------------------
black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
green = (0,255,0)
red = (255,0,0)
random = (200, 120, 4)

#---------------------Variables-------------------
car_radius = 20
car_x = 40
car_y = 600
car_max_speed = 3
#Angle in rad (0 = faced straight right)
car_angles = [-0.785, -0.392,0,0.392,0.785]
rt_angles = car_angles

#------------------------Init---------------------
clock = pygame.time.Clock()
pygame.init()
font = pygame.font.Font(None, 30)
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Cars')
level_img = pygame.image.load('test_rewards.png')

gameDisplay.blit(level_img, (0,0))

def mutation(x):
    if random.randrange(0,1)<0.1:
        offset = np.random.normal()*0.5
        newx = x + offset
        return newx
    else:
        return x

class pickup:
	def __init__(self, x,y,color = green, width = 5, height = 5, pickup_reward = 1):
		self.x = x
		self.y = y
		self.color = color
		self.width = width
		self.height = height
		self.pickup_reward = pickup_reward

	def draw(self, gameDisplay):
		pygame.draw.rect(gameDisplay, self.color, [self.x,self.y,self.width,self.height])


class Sensor:
    def __init__(self,x,y,dist, angle,color = green, width = 2, height = 2):
        self.dist = dist
        self.angle = angle
        self.x = x + np.cos(self.angle)*self.dist
        self.y = y + np.sin(self.angle)*self.dist
        self.color = color
        self.width = width
        self.height = height
        #Default value, white
        self.value = 0
        
    def update(self,x,y, direction):
        self.x =x + np.cos(self.angle + direction)*self.dist
        self.y =y + np.sin(self.angle + direction)*self.dist
        self.value, self.color = self.read_color()

    def draw(self, gameDisplay):
        pygame.draw.rect(gameDisplay, self.color, [self.x,self.y,self.width,self.height])

    def read_color(self):
        if tuple(level_img.get_at((int(self.x),int(self.y)))) == (0,0,0,255):
            #black
            return 1, green
        else:
        	#white
        	return 0, blue
            

class Car:
    def __init__(self,x,y,radius,angles,color, max_speed, brain):
        self.max_speed = max_speed
        self.score = 0
        self.fitness = 0
        self.x = x
        self.y = y
        self.color = color
        self.is_accelerating = False
        self.is_rotating = 0
        self.angles = angles
        self.turning_intensity = 0.2
        self.direction = angles[2]
        self.radius = radius
        self.sensors = []
        self.hitbox = []
        self.velocity = 0
        self.acceleration_factor = 1
        self.friction_factor = 0.6
        if(isinstance(brain, nn.NeuralNetwork)):
            self.brain = brain.copy()
            self.brain.mutate(mutation)
        else:
            self.brain = nn.NeuralNetwork(5,8,2)
        self.init_sensors()
        self.init_hitbox()

    def init_sensors(self):
        for angle in self.angles:
            for i in range(2,5):
                sensor = Sensor(self.x,self.y, 15*i, angle)
                self.sensors.append(sensor)

    def init_hitbox(self):
    	for angle in self.angles:
    		collider = Sensor(self.x, self.y, self.radius, angle, color = random)
    		self.hitbox.append(collider)

    def copy(self):
        return Car(car_x,car_y,self.brain)

    def think(self):
        #TODO implement inputs & actions
        pass

    def draw(self, gameDisplay):
        pygame.draw.circle(gameDisplay, self.color,(int(self.x),int(self.y)),self.radius)
        for sensor in self.sensors:
            sensor.draw(gameDisplay)
        for sensor in self.hitbox:
        	sensor.draw(gameDisplay)

    def update(self, gameDisplay,draw=False):
        self.direction += self.is_rotating*self.turning_intensity
        self.velocity += self.is_accelerating* self.acceleration_factor
        self.velocity -= self.friction_factor
        if self.velocity < 0:
            self.velocity = 0
        self.x += np.cos(self.direction)*self.velocity
        self.y += np.sin(self.direction)*self.velocity
        for sensor in self.sensors:
            sensor.update(self.x,self.y, self.direction)
        for collider in self.hitbox:
        	collider.update(self.x, self.y, self.direction)
        if draw:
            self.draw(gameDisplay)

    def collision(self):
    	for collider in self.hitbox:
    		if collider.value == 1:
    			return True
    		else:
    			return False

    def sensors_seeing_wall(self):
        for sensor in self.sensors:
            if sensor.value == 1:
                return True
        return False

class Level:
    def __init__(self, img):
        self.img = img

    def draw(self, gameDisplay):
        gameDisplay.blit(self.img, (0,0))

def get_inputs(rotating, accelerating):
    exit = False
    for event in pygame.event.get():
        if event.type ==pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                exit = True
            elif event.key == pygame.K_UP:
                accelerating = 1
            elif event.key == pygame.K_LEFT:
                rotating = -1
            elif event.key == pygame.K_RIGHT:
                rotating = 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                accelerating = 0
            elif event.key == pygame.K_LEFT:
                rotating = 0
            elif event.key == pygame.K_RIGHT:
                rotating = 0
    return exit, accelerating, rotating

def show_fps(gameDisplay):
    text = font.render(str(int(clock.get_fps())), True, blue)
    gameDisplay.blit(text, (5,5))

def main():

    car = Car(car_x,car_y,car_radius,car_angles,red,car_max_speed, None)
    level = Level(level_img)
    exit = False

    while not exit:

        exit, car.is_accelerating, car.is_rotating = get_inputs(car.is_rotating, car.is_accelerating)
        car.update(gameDisplay)

        gameDisplay.fill(white)
        level.draw(gameDisplay)
        car.draw(gameDisplay)
        show_fps(gameDisplay)

        if(car.collision()):
        	pass
        	exit = True

        pygame.display.update()
        clock.tick(60)



if __name__ == "__main__":

    main()
