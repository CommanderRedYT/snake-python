import pygame
import random

class Food:
    def __init__(self, maxX, maxY, minX, minY, screen: pygame.Surface):
        self.screen = screen
        self.maxX = maxX
        self.maxY = maxY
        self.minX = minX
        self.minY = minY
        self.update()
    

    def draw(self):
        pygame.draw.rect(self.screen, (255, 0, 0), (self.positionX, self.positionY, 10, 10))

    def update(self):
        self.positionX = random.randint(self.minY, self.maxX)
        self.positionY = random.randint(self.minX, self.maxY)

    
    

