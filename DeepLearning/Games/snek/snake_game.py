import pygame
import math
import numpy as np
from snek import Snake, Pickup
from colors import Color_Palette
import time
import sys

#Grid dimensions
CELL_SIZE = 40
GRID_SIZE_X = 20
GRID_SIZE_Y = 30

#Display dimensions
display_height = GRID_SIZE_X*CELL_SIZE
display_width = GRID_SIZE_Y*CELL_SIZE

#Snake start variables
START_Y = 12*CELL_SIZE
START_X = 12*CELL_SIZE
INITIAL_SIZE = 20

#Colors
colors = Color_Palette()

#Fonts
pygame.init()

small_text = pygame.font.Font('font.ttf', 30)
large_text = pygame.font.Font('font.ttf',50)

class Gamestate():
    def __init__(self):
        self.snake = Snake(START_X, START_Y, None,CELL_SIZE)
        self.pickup = Pickup(self.snake, CELL_SIZE)

    def reset(self):
        self.snake = Snake(START_X, START_Y, None,CELL_SIZE)
        self.pictail_coordskup = Pickup(self.snake, CELL_SIZE)


def message_display(text, display):
    text = large_text.render(text, True, colors.colors[0])
    gameDisplay.blit(text, (display_width/2,display_height/2))

def show_current_score(display, game):
	text = small_text.render(""+str(len(game.snake.parts)-INITIAL_SIZE), True, colors.colors[1])
	gameDisplay.blit(text, (15,35))

def show_hint(display, alpha):
    text = small_text.render("Welcome to Snek - Press 'x' to leave",0, colors.colors[3])
    text.set_alpha(alpha)
    gameDisplay.blit(text, (display_width-600,55))

def draw(game_state, display):
    game_state.pickup.draw(display)
    game_state.snake.draw(display)


def get_input():
    events = pygame.event.get()
    space = False
    dir = None
    exit = False
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dir = (-1,0)
            elif event.key == pygame.K_RIGHT:
                dir = (1,0)
            elif event.key == pygame.K_UP:
                dir = (0,-1)
            elif event.key == pygame.K_DOWN:
                dir = (0,1)
            elif event.key == pygame.K_SPACE:
                space = True
            elif event.key == pygame.K_x:
                exit = True
    return dir, space, exit

def is_game_over(game):
    for i in range(1,len(game.snake.parts)):
        if game.snake.head_x() == game.snake.parts[i].x and game.snake.head_y() == game.snake.parts[i].y:
            #deaderino
            return True
    return False

def update(game_state):
    dir, space, exit = get_input()
    #dont allow 180° turns
    if dir and not (game_state.snake.dir[0] == -dir[0] or game_state.snake.dir[1] == -dir[1]):
        game_state.snake.dir = dir
    #move a step
    game_state.snake.move()
    #check if hit a pickup
    hit_pickup = False
    if game_state.pickup.x == game_state.snake.head_x() and game_state.pickup.y == game_state.snake.head_y():
        hit_pickup = True
        game_state.snake.eat_pickup(game_state.pickup.color)
        game_state.pickup =Pickup(game_state.snake,CELL_SIZE)
    #check if hit own tail
    return exit


def game_over(game, display):
    message_display('Game Over',display)

def main():
    exit = False
    game_state = Gamestate()
    alpha =100

    while not exit:
        gameDisplay.fill(colors.grey)
        draw(game_state,gameDisplay)
        show_current_score(gameDisplay, game_state)
        if alpha >0:
            show_hint(gameDisplay, alpha)
        alpha -=2
        exit = update(game_state)
        if is_game_over(game_state):
            game_over(game_state, gameDisplay)
            pygame.display.update()
            pygame.time.wait(3000)
            game_state.reset()
        pygame.display.update()
        clock.tick(60)
        pygame.time.wait(60)


if __name__ == '__main__':
	clock = pygame.time.Clock()
	gameDisplay = pygame.display.set_mode((display_width,display_height))
	pygame.display.set_caption('Snake')

	main()
