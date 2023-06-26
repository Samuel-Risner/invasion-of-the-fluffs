from sys import exit as sys_exit
import json

import pygame
from pygame.locals import QUIT, VIDEORESIZE, RESIZABLE, KEYDOWN, KSCAN_F11, K_f, K_F11, FULLSCREEN, MOUSEBUTTONUP, \
    K_UP, K_DOWN, K_LEFT, K_RIGHT, K_1, K_2, K_3, K_4, K_5, K_q, K_w, K_e, K_r, K_t, K_z, K_u, K_i, K_o, K_n, K_m

from asset_handler import AssetHandler
from settings import TILES_HEIGHT_SMALL, TILES_WIDTH
pygame.init()

BLACK = (0, 0, 0, 255)

SCREEN_MIN_WIDTH = 500
SCREEN_MIN_HEIGHT = 500
screen_width = SCREEN_MIN_WIDTH
screen_height = SCREEN_MIN_HEIGHT

monitor_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
screen = pygame.display.set_mode((screen_width, screen_height), RESIZABLE)

CLOCK = pygame.time.Clock()
fullscreen = False

CANVAS = pygame.Surface((SCREEN_MIN_WIDTH, SCREEN_MIN_HEIGHT))

canvas_scale = [SCREEN_MIN_WIDTH, SCREEN_MIN_HEIGHT]
canvas_pos = [0, 0]

asset_handler = AssetHandler()

def on_size_change():
    w = screen.get_width()
    h = screen.get_height()

    h_rel = SCREEN_MIN_WIDTH / SCREEN_MIN_HEIGHT
    w_rel = SCREEN_MIN_HEIGHT / SCREEN_MIN_WIDTH

    h_new = w * w_rel
    w_new = h * h_rel

    if w_new > w:
        canvas_scale[0] = w
        canvas_scale[1] = h_new
    else:
        canvas_scale[0] = w_new
        canvas_scale[1] = h

    canvas_pos[0] = (w - canvas_scale[0]) / 2
    canvas_pos[1] = (h - canvas_scale[1]) / 2

def get_mouse_pos() -> tuple[int, int]:
    x, y = pygame.mouse.get_pos()
    x = int((x / screen.get_width()) * SCREEN_MIN_WIDTH)
    y = int((y / screen.get_height()) * SCREEN_MIN_HEIGHT)

    return x, y

class Tile():

    def __init__(
        self,
        asset_handler:AssetHandler,
        x:int,
        y:int,
        tile_contents,
        tile_type:int):

        self.asset_handler = asset_handler

        self.tile_contents = tile_contents

        self.tile_type = tile_type

        self.rect = pygame.Rect(x, y, TILES_WIDTH, TILES_HEIGHT_SMALL)

        self.surf = self.asset_handler.ALL_TILES[tile_type][-1]

    def create_surf(self):            
        self.surf = pygame.Surface((TILES_WIDTH, TILES_HEIGHT_SMALL))
        self.surf.set_colorkey(BLACK)
        self.surf.blit(self.asset_handler.ALL_TILES[self.tile_type][-1], (0, 0))
        if self.tile_contents != -1:
            self.surf.blit(self.asset_handler.TILE_CONTENTS[self.tile_contents], (0, 0))
        self.surf = self.surf.convert_alpha()

    def draw(self, surf:pygame.Surface):
        surf.blit(self.surf, self.rect.topleft)

    def collision(self, pos:tuple[int, int]):
        temp = pygame.Rect(self.rect.x + TILES_WIDTH / 4, self.rect.y + TILES_HEIGHT_SMALL / 4, TILES_WIDTH / 2, TILES_HEIGHT_SMALL / 2)
        if temp.collidepoint(pos):
            return True

        return False

tiles = [
    [Tile(asset_handler, 0, 0, 0, 1), Tile(asset_handler, TILES_WIDTH, 0, 0, 1)],
    [Tile(asset_handler, TILES_WIDTH / 2, TILES_HEIGHT_SMALL / 2, 0, 1), Tile(asset_handler, TILES_WIDTH + TILES_WIDTH / 2, TILES_HEIGHT_SMALL / 2, 0, 1)]
]

def on_exit():
    result = list()

    for l in tiles:
        for t in l:
            result.append([t.tile_contents, t.tile_type, True, True])
        result.append([0])

    with open("lvls/result.json", "w") as d:
        json.dump(result, d)

    pygame.quit()
    sys_exit()

next_tile_type = 0
next_tile_contents = -1
next_mode = True

while True:
    CLOCK.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            on_exit()

        if event.type == VIDEORESIZE:
            if not fullscreen:
                screen_width, screen_height = event.w, event.h

                if screen_width < SCREEN_MIN_WIDTH:
                    screen_width = SCREEN_MIN_WIDTH
                if screen_height < SCREEN_MIN_HEIGHT:
                    screen_height = SCREEN_MIN_HEIGHT

                screen = pygame.display.set_mode((screen_width, screen_height), RESIZABLE)

                on_size_change()

        if event.type == KEYDOWN:

            if event.key in (KSCAN_F11, K_F11, K_f):
                fullscreen = not fullscreen

                if fullscreen:
                    screen = pygame.display.set_mode(monitor_size, FULLSCREEN)
                    on_size_change()
                else:
                    screen = pygame.display.set_mode(
                        (screen_width, screen_height),
                        RESIZABLE
                    )

            elif event.key == K_UP:
                for l in tiles:
                    for t in l:
                        t.rect.y += TILES_HEIGHT_SMALL

            elif event.key == K_DOWN:
                for l in tiles:
                    for t in l:
                        t.rect.y -= TILES_HEIGHT_SMALL

            elif event.key == K_LEFT:
                for l in tiles:
                    for t in l:
                        t.rect.x += TILES_WIDTH
            
            elif event.key == K_RIGHT:
                for l in tiles:
                    for t in l:
                        t.rect.x -= TILES_WIDTH

            elif event.key == K_1:
                next_tile_type = 0

            elif event.key == K_2:
                next_tile_type = 1

            elif event.key == K_3:
                next_tile_type = 2

            elif event.key == K_4:
                next_tile_type = 3

            elif event.key == K_5:
                next_tile_type = 4

            elif event.key == K_q:
                next_tile_contents = -1

            elif event.key == K_w:
                next_tile_contents = 0

            elif event.key == K_e:
                next_tile_contents = 1

            elif event.key == K_r:
                next_tile_contents = 2

            elif event.key == K_t:
                next_tile_contents = 3

            elif event.key == K_z:
                next_tile_contents = 4

            elif event.key == K_u:
                next_tile_contents = 5

            elif event.key == K_i:
                next_tile_contents = 6

            elif event.key == K_o:
                next_tile_contents = 7

            elif event.key == K_m:
                for l in tiles:
                    l.append(Tile(asset_handler, l[-1].rect.x + TILES_WIDTH, l[-1].rect.y, -1, 1))

            elif event.key == K_n:
                l = list()
                x = 0
                y = tiles[-1][-1].rect.y + TILES_HEIGHT_SMALL / 2

                x_1 = tiles[-1][0].rect.x
                x_2 = tiles[-2][0].rect.x

                if x_1 > x_2:
                    x = x_2
                else:
                    x = x_1+ TILES_WIDTH / 2

                for i in range(0, len(tiles[0]), 1):
                    l.append(Tile(asset_handler, x, y, -1, 1))
                    x += TILES_WIDTH

                tiles.append(l)


            print("Tiletype", next_tile_type)
            print("Tilecontents", next_tile_contents)
            print()

        if event.type == MOUSEBUTTONUP:
            if pygame.mouse.get_focused():
                pos = get_mouse_pos()

                for l in tiles:
                    for t in l:
                        if t.collision(get_mouse_pos()):
                            t.tile_contents = next_tile_contents
                            t.tile_type = next_tile_type
                            t.create_surf()
                            break

    CANVAS.fill(BLACK)

    for l in tiles:
        for t in l:
            t.draw(CANVAS)

    screen.blit(
        pygame.transform.scale(
            CANVAS, canvas_scale
        ).convert_alpha(), canvas_pos
    )

    pygame.display.update()