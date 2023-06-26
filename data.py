import pygame
from pygame import RESIZABLE

from asset_handler import AssetHandler
from settings import SCREEN_INIT_WIDTH, SCREEN_INIT_HEIGHT

class Data():

    def __init__(self):
        self.monitor_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self.fullscreen = False
        self.screen_width, self.screen_height = SCREEN_INIT_WIDTH, SCREEN_INIT_HEIGHT

        self.screen = pygame.display.set_mode((SCREEN_INIT_WIDTH, SCREEN_INIT_HEIGHT), RESIZABLE)
        pygame.display.set_caption("Invasion of the fluffs!")
        self.CANVAS = pygame.Surface((SCREEN_INIT_WIDTH, SCREEN_INIT_HEIGHT))

        self.asset_handler = AssetHandler()
        pygame.display.set_icon(self.asset_handler.TILE_CONTENTS[4])

        self.canvas_scale = [SCREEN_INIT_WIDTH, SCREEN_INIT_HEIGHT]
        self.canvas_pos = [0, 0]

        self.CLOCK = pygame.time.Clock()

        self.screen_rect = pygame.Rect(0, 0, SCREEN_INIT_WIDTH, SCREEN_INIT_HEIGHT)

    def on_size_change(self):
        w = self.screen.get_width()
        h = self.screen.get_height()

        h_rel = SCREEN_INIT_WIDTH / SCREEN_INIT_HEIGHT
        w_rel = SCREEN_INIT_HEIGHT / SCREEN_INIT_WIDTH

        h_new = w * w_rel
        w_new = h * h_rel

        if w_new > w:
            self.canvas_scale[0] = w
            self.canvas_scale[1] = h_new
        else:
            self.canvas_scale[0] = w_new
            self.canvas_scale[1] = h

        self.canvas_pos[0] = (w - self.canvas_scale[0]) / 2
        self.canvas_pos[1] = (h - self.canvas_scale[1]) / 2

        self.screen_rect.x = self.canvas_pos[0]
        self.screen_rect.y = self.canvas_pos[1]
        self.screen_rect.w = self.canvas_scale[0]
        self.screen_rect.h = self.canvas_scale[1]

    def get_mouse_pos(self) -> tuple[int, int]:
        x, y = pygame.mouse.get_pos()
        x = (x / self.screen.get_width()) * SCREEN_INIT_WIDTH
        y = (y / self.screen.get_height()) * SCREEN_INIT_HEIGHT

        return x, y

    def is_on_screen(self, rect:pygame.Rect) -> bool:
        return self.screen_rect.colliderect(rect)