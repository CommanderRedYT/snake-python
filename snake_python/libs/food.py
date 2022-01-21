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
        self.positionX = random.randint(self.minY, self.maxX)
        self.positionY = random.randint(self.minX, self.maxY)
    
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

    
    

