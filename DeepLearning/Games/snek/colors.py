import random
import pygame

class Color_Palette():
    def __init__(self):
        self.colors=[]
        self.grey = pygame.Color('0x3b4252')
        self.red = pygame.Color('0xbf616a')
        self.green = pygame.Color('0xa3be8c')
        self.yellow = pygame.Color('0xebcb8b')
        self.blue = pygame.Color('0x81a1c1')
        self.purple = pygame.Color('0xb48ead')
        self.light_gray = pygame.Color('0x4c566a')
        self.colors.append(pygame.Color('0xbf616a'))
        self.colors.append(pygame.Color('0xa3be8c'))
        self.colors.append(pygame.Color('0xebcb8b'))
        self.colors.append(pygame.Color('0x81a1c1'))
        self.colors.append(pygame.Color('0xb48ead'))

    def random_color(self):
        return self.colors[random.randrange(len(self.colors))]
