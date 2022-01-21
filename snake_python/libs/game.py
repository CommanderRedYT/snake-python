#!/usr/bin/python3
import os
from .food import Food

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # hide pygame support prompt
import pygame

from .snake import Direction, Snake


class Game:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.title = "Snake"
        self.bg_color = (0, 0, 0)
        self.screen = None
        self.snakes = []
        self.gameover = False
        self.init()

    def init(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.screen.fill(self.bg_color)
        self.snakes.append(
            Snake(self.width / 2, self.height / 2, pygame.Color(255, 255, 255), self.screen, self.handleGameover)
        )
        self.food = Food(400, 400, 0, 0, self.screen)
        self.food.draw()

    def getPlayerSnake(self) -> Snake | None:
        for s in self.snakes:
            if not s.isGuest():
                return s
        return None

    def handleGameover(self):
        self.gameover = True
        self.screen.fill(pygame.Color(0, 0, 0))
        self.screen.blit(
            pygame.font.SysFont("monospace", 48).render("Game Over", True, pygame.Color(255, 255, 255)),
            (self.width / 2 - 100, self.height / 2 - 10)
        )
        pygame.display.update()
        pygame.time.wait(2000)
        pygame.quit()
        quit()

    def run(self):
        iterations = 0
        while not self.gameover:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    player = self.getPlayerSnake()
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        if player.getDirection() != Direction.DOWN:
                            player.setDirection(Direction.UP)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if player.getDirection() != Direction.UP:
                            player.setDirection(Direction.DOWN)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        if player.getDirection() != Direction.RIGHT:
                            player.setDirection(Direction.LEFT)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        if player.getDirection() != Direction.LEFT:
                            player.setDirection(Direction.RIGHT)
                    elif event.key == pygame.K_c:
                        self.screen.fill(pygame.Color(0, 0, 0))
                    elif event.key == pygame.K_TAB:
                        player.add_segment()
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()

            self.update()

            pygame.display.update()

            # Little easter-egg, draw the game screen into the icon
            iterations += 1
            if iterations > 1200:
                pygame.display.set_icon(self.screen)
                iterations = 0

    def update(self):
        for snake in self.snakes:
            snake.update()
