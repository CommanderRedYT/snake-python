#!/usr/bin/python3
import dns.resolver
from .snake import Direction, Snake, Difficulty
import pygame_menu
import pygame
import os
import asyncio
import websockets

from .food import Food

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"  # hide pygame support prompt


class MessageHandler:
    pass


class Game:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.title = "Snake"
        self.bg_color = (0, 0, 0)
        self.screen = None
        self.snakes = []
        self.gameover = False
        self.mode = Difficulty.NORMAL
        self.init()
        self.messageHandler = None
        self.server = ""

    def init(self):
        pygame.init()
        self.gameover = False
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.showMainMenu()
        self.screen.fill(self.bg_color)
        self.snakes.append(
            Snake(self.width / 2, self.height / 2, pygame.Color(255,
                  255, 255), self.screen, self.handleGameover, self.mode)
        )
        self.food = Food(self.screen.get_width(
        ) - 40, self.screen.get_height() - 40, 40, 40, 20, 20, self.screen)
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
            pygame.font.SysFont("monospace", 48).render(
                "Game Over", True, pygame.Color(255, 255, 255)),
            (self.width / 2 - 100, self.height / 2 - 10)
        )
        self.screen.blit(
            pygame.font.SysFont("monospace", 48).render("Score: " + str(self.getPlayerSnake().getScore()), True, pygame.Color(255, 255, 255)),
            (self.width / 2 - 100, self.height / 2 + 30)
        )
        pygame.display.update()
        pygame.time.wait(2000)
        self.snakes = []
        self.init()

    def setServer(self, server):
        self.server = server

    def showMainMenu(self):
        def startGame():
            if self.server != "":
                print(self.server)
                self.messageHandler = MessageHandler(self.screen, self)
                print(self.messageHandler.setServer(self.server))
                self.messageHandler.start()
            self.mainMenu.disable()

        def setEasyMode(toggled):
            self.mode = Difficulty.EASY if toggled else Difficulty.NORMAL

        self.mainMenu = pygame_menu.Menu("Snake", self.screen.get_width(
        ), self.screen.get_height(), theme=pygame_menu.themes.THEME_BLUE)
        self.mainMenu.add.button("Start", startGame)
        self.mainMenu.add.toggle_switch(
            "Easy mode", (self.mode == Difficulty.EASY), setEasyMode)
        print(self.server)
        self.mainMenu.add.text_input(
            "Server: ", default='', onchange=self.setServer)
        self.mainMenu.mainloop(self.screen)

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
            self.food.checkCollision(self.getPlayerSnake())

            pygame.display.update()

            # Little easter-egg, draw the game screen into the icon
            iterations += 1
            if iterations > 1200:
                pygame.display.set_icon(self.screen)
                iterations = 0

    def update(self):
        for snake in self.snakes:
            snake.update()


class MessageHandler:
    def __init__(self, screen: pygame.Surface, game: Game) -> None:
        self.screen = screen
        self.game = game
        self.ws = None
        self.ip = None

    def setServer(self, domainOrIp: str) -> str:
        # if domainOrIp is an IP, check if port is specified in domainOrIp (e.g. with splitting by ":") and return it
        # if domainOrIp is a domain, check for SRV records and return the port for _python_snake._tcp
        # if no SRV record is found, return the default port (39999)
        if domainOrIp.count(":") == 1:
            self.ip = domainOrIp
            return domainOrIp

        try:
            ip = dns.resolver.query(domainOrIp, "A")[0].to_text()
            if ":" in ip:
                self.ip = ip
                return ip
            else:
                self.ip = ip + ":39999"
                return ip + ":39999"
        except:
            try:
                srv = dns.resolver.query(domainOrIp, "SRV")[0].to_text()
                print(srv)
                self.ip = srv.split(" ")[3]
                return srv.split(" ")[3]
            except:
                self.ip = domainOrIp + ":39999"
                return domainOrIp + ":39999"

    async def __websocket__(self):
        async with websockets.connect(f"ws://{self.ip}") as ws:
            self.ws = ws
            print(await self.ws.recv())

    def start(self):
        asyncio.run(self.__websocket__())
