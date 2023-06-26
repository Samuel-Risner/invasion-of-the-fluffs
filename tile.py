import pygame

from asset_handler import AssetHandler
from settings import TILES_HEIGHT_LARGE, TILES_WIDTH, TILES_HEIGHT_SMALL, BLACK, TRAVERSABLE_TILE_CONTENT_TYPES

class Tile():

    def __init__(
        self,
        asset_handler:AssetHandler,
        x:int,
        y:int,
        tile_contents,
        tile_type:int,
        visible:bool,
        traversed:bool,
        top_left = None,
        top_right = None,
        bottom_left = None,
        bottom_right = None):

        self.asset_handler = asset_handler

        self.top_left = top_left
        self.top_right = top_right
        self.bottom_left = bottom_left
        self.bottom_right = bottom_right
        self.adjacent_tiles = (self.top_left, self.top_right, self.bottom_left, self.bottom_right)

        self.tile_contents = tile_contents

        self.tile_type = tile_type
        self.draw_type = 0

        self.rect = pygame.Rect(x, y, TILES_WIDTH, TILES_HEIGHT_SMALL)
        self.visible = visible
        self.traversed = traversed
        self.traversable = False

        self.surf = self.asset_handler.ALL_TILES[tile_type][self.draw_type]

        self.is_stopper = False

        self.update_traversable()

    def update_traversable(self):
        self.traversable = self.tile_contents in TRAVERSABLE_TILE_CONTENT_TYPES

    def create_surf(self):
        bl = self.bottom_left
        br = self.bottom_right
        h = TILES_HEIGHT_LARGE

        if bl.visible and br.visible:
            self.draw_type = 3
            h = TILES_HEIGHT_SMALL
        elif bl.visible:
            self.draw_type = 2
        elif bl.visible:
            self.draw_type = 1
        else:
            self.draw_type = 0
            
        self.surf = pygame.Surface((TILES_WIDTH, h))
        self.surf.set_colorkey(BLACK)
        self.surf.blit(self.asset_handler.ALL_TILES[self.tile_type][self.draw_type], (0, 0))
        if self.tile_contents != -1:
            self.surf.blit(self.asset_handler.TILE_CONTENTS[self.tile_contents], (0, 0))
        self.surf = self.surf.convert_alpha()

    def show(self, surf:pygame.Surface):
        surf.blit(self.surf, self.rect.topleft)

    def draw(self, surf:pygame.Surface):
        if self.visible:
            surf.blit(self.surf, self.rect.topleft)

    def show_surroundings(self):
        if not self.top_left.is_stopper:
            self.top_left.visible = True

        if not self.top_right.is_stopper:
            self.top_right.visible = True

        if not self.bottom_left.is_stopper:
            self.bottom_left.visible = True

        if not self.bottom_right.is_stopper:
            self.bottom_right.visible = True

        # self.top_right.visible = True
        # self.bottom_left.visible = True
        # self.bottom_right.visible = True
        
        
        # self.bottom_left.visible = True
        # self.bottom_right.visible = True

        self.create_surf()
        self.top_left.create_surf()
        self.top_right.create_surf()
        self.bottom_left.create_surf()
        self.bottom_right.create_surf()
    