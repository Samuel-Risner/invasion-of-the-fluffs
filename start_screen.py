import pygame
from pygame import QUIT, VIDEORESIZE, RESIZABLE, KEYDOWN, KSCAN_F11, K_F11, FULLSCREEN, MOUSEBUTTONDOWN

from settings import SCREEN_INIT_HEIGHT, SCREEN_INIT_WIDTH, SCREEN_MIN_WIDTH, SCREEN_MIN_HEIGHT, FPS, BLACK
from data import Data

class StartScreen():

    def __init__(self, data:Data):
        self.DATA = data
        self.text = None
        self.text_pos = [0, 0]
        self.set_text(-1)

    def start(self) -> bool:
        while True:
            self.DATA.CLOCK.tick(FPS)

            for event in pygame.event.get():
                if event.type == QUIT:
                    return True

                if event.type == VIDEORESIZE:
                    if not self.DATA.fullscreen:
                        self.DATA.screen_width, self.DATA.screen_height = event.w, event.h

                        if self.DATA.screen_width < SCREEN_MIN_WIDTH:
                            self.DATA.screen_width = SCREEN_MIN_WIDTH
                        if self.DATA.screen_height < SCREEN_MIN_HEIGHT:
                            self.DATA.screen_height = SCREEN_MIN_HEIGHT

                        self.DATA.screen = pygame.display.set_mode(
                            (self.DATA.screen_width, self.DATA.screen_height),
                            RESIZABLE
                        )
                        self.DATA.on_size_change()

                if event.type == KEYDOWN:

                    if event.key in (KSCAN_F11, K_F11):
                        self.DATA.fullscreen = not self.DATA.fullscreen

                        if self.DATA.fullscreen:
                            self.DATA.screen = pygame.display.set_mode(self.DATA.monitor_size, FULLSCREEN)
                            self.DATA.on_size_change()
                        else:
                            self.DATA.screen = pygame.display.set_mode(
                                (self.DATA.screen_width, self.DATA.screen_height),
                                RESIZABLE
                            )
                    else:
                        return False
                    
                if event.type == MOUSEBUTTONDOWN:
                    return False

            self.DATA.CANVAS.fill(BLACK)

            self.DATA.CANVAS.blit(self.text, self.text_pos)

            self.DATA.screen.blit(
                pygame.transform.scale(
                    self.DATA.CANVAS, self.DATA.canvas_scale
                ).convert_alpha(), self.DATA.canvas_pos)

            pygame.display.update()

    def save(self):
        pass

    def reset(self):
        pass

    def set_text(self, i:int):
        font = self.DATA.asset_handler.FONT
        if i == -1:
            self.text = font.render3(["Welcome!", "Press anything to start!"])
        elif i == 1:
            self.text = font.render3(["Welcome back!"])
        elif i == 2:
            self.text = font.render3(["Welcome back!", "Your life was depleted."])
        elif i == 3:
            self.text = font.render3(["Welcome back!", "Seems like some persons brains were eaten..."])
        elif i == 4:
            self.text = font.render3(["Welcome back!", "Your mission was a complete success!"])
        else:
            self.text = font.render3(["Welcome back!", "Why are you here?"])

        self.text_pos[0] = SCREEN_INIT_WIDTH / 2 - self.text.get_width() / 2
        self.text_pos[1] = SCREEN_INIT_HEIGHT / 2 - self.text.get_height() / 2