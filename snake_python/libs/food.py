import pygame
import random
from .snake import Snake

class Food:
    def __init__(self, maxX, maxY, minX, minY, width, height, screen: pygame.Surface):
        self.screen = screen
        self.maxX = maxX
        self.maxY = maxY
        self.minX = minX
        self.minY = minY
        self.width = width
        self.height = height
        self.update()
    

    def draw(self):
        self.rect = pygame.Rect(self.positionX, self.positionY, self.width, self.height)
        pygame.draw.rect(self.screen, (255, 0, 0), self.rect)

    def update(self):
        # self.positionX = random.randint(self.minY, self.maxX)
        # self.positionY = random.randint(self.minX, self.maxY)

        # position needs to be aligned with the grid (self.width)
        self.positionX = random.randint(int(self.minY / self.width), int(self.maxX / self.width)) * self.width
        self.positionY = random.randint(int(self.minX / self.width), int(self.maxY / self.width)) * self.width
    
    def clearFood(self):
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect)

    def checkCollision(self, snake: Snake) -> bool:
        collides = self.rect.colliderect(snake.getHead())
        if collides:
            self.clearFood()
            self.update()
            self.draw()
            snake.add_segment()
        return collides

    
    

