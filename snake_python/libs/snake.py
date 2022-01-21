#!/usr/bin/python3
from enum import Enum

from time import time
import pygame

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class OppositeDirection(Enum):
    UP = 1
    DOWN = 0
    LEFT = 3
    RIGHT = 2


class Snake:
    def __init__(self, x: int, y: int, color: pygame.Color, screen: pygame.Surface, gameover, moves: bool = True) -> None:
        self.x = int(x)
        self.y = int(y)
        self.color = color
        self.segments = []
        self.map = [[0]*screen.get_height()]*screen.get_width()
        self.direction = Direction.RIGHT
        self.iterations = 0
        self.screen = screen
        self.width = 20
        self.length = 0
        self.add_segments(5)
        self.moves = moves
        self.gameover = gameover

    def __len__(self) -> int:
        return len(self.segments)

    def setDirection(self, direction: Direction) -> None:
        self.direction = direction

    def getDirection(self) -> Direction:
        return self.direction

    def update(self) -> None:

        if self.moves:
            self.iterations += 1

            if self.iterations % 300 != 0:
                return
            
            if self.direction == Direction.UP:
                self.y -= self.width
            elif self.direction == Direction.DOWN:
                self.y += self.width
            elif self.direction == Direction.LEFT:
                self.x -= self.width
            elif self.direction == Direction.RIGHT:
                self.x += self.width

            if self.x < 0:
                self.x = self.screen.get_width() - self.width
            elif self.x > self.screen.get_width() - self.width:
                self.x = 0
            elif self.y < 0:
                self.y = self.screen.get_height() - self.width
            elif self.y > self.screen.get_height() - self.width:
                self.y = 0

            for segment in self.segments:
                segment.update()

            if int(self.map[self.x][self.y]) > int(time()) and not self.isGuest(): # this is not working, please fix
                self.gameover()
                return

            self.segments.insert(0, Segment(self.x, self.y, self.width, self.color, self))

    def add_segment(self) -> None:
        self.segments.append(Segment(self.x, self.y, self.width, self.color, self))
        self.length += 1

    def add_segments(self, ammount) -> None:
        for i in range(ammount):
            self.add_segment()

    def isGuest(self) -> bool:
        return False


class GuestSnake(Snake):
    def __init__(self, x: int, y: int, color: pygame.Color, screen: pygame.Surface) -> None:
        super().__init__(x, y, color, screen, None, False)

    def isGuest(self) -> bool:
        return True


class Segment:
    def __init__(self, x, y, width, color: pygame.Color, snake: Snake) -> None:
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.counter = 0
        self.snake = snake
        snake.map[x][y] = time()
        self.draw()

    def draw(self) -> None:
        pygame.draw.rect(self.snake.screen, self.color, (self.x, self.y, self.width, self.width))

    def update(self) -> None:
        self.counter += 1
        if self.counter >= self.snake.length:
            pygame.draw.rect(self.snake.screen, (0, 0, 0), (self.x, self.y, self.width, self.width))
            self.snake.segments.remove(self)
            self.snake.map[self.x][self.y] = 0