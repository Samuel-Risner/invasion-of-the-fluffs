import pygame
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_s, K_a, K_d, K_RETURN

from asset_handler import AssetHandler
from tile import Tile
from settings import TRAVERSABLE_TILE_CONTENT_TYPES, PLAYER_WIDTH, PLAYER_HEIGHT

class Player():

    def __init__(self, asset_handler:AssetHandler, spawn_tile:Tile):
        self.asset_handler = asset_handler
        self.current_tile = spawn_tile

        self.current_tile.traversed = True
        self.current_tile.visible = True
        self.current_tile.show_surroundings()

        self.pos = [0, 0]
        self.calculate_pos()

        self.selected = False
        self.selected_tile = spawn_tile

    # def _move(self, tile_goal:Tile) -> bool:
    #     if tile_goal.tile_type in TRAVERSABLE_TILE_CONTENT_TYPES:
    #         self.current_tile = tile_goal
    #         tile_goal.traversed = True
    #         tile_goal.show_surroundings()
            
    #         return True

    #     return False

    # def move_top_left(self) -> bool:
    #     return self._move(self.current_tile.top_left)

    # def move_top_right(self) -> bool:
    #     return self._move(self.current_tile.top_left)

    # def move_bottom_left(self) -> bool:
    #     return self._move(self.current_tile.top_left)

    # def move_bottom_right(self) -> bool:
    #     return self._move(self.current_tile.top_left)

    def calculate_pos(self):
        x = self.current_tile.rect.x + self.current_tile.rect.w / 2 - PLAYER_WIDTH / 2
        y = self.current_tile.rect.y + self.current_tile.rect.h / 2 - PLAYER_HEIGHT

        self.pos[0] = x
        self.pos[1] = y

    def draw(self, surf:pygame.Surface):
        surf.blit(self.asset_handler.PLAYER, self.pos)

        if self.selected:
            surf.blit(self.asset_handler.HIGHLIGHTS[0], self.selected_tile.rect.topleft)

    def undo_selected(self):
        self.selected = False
        self.selected_tile = self.current_tile

    def on_key_press(self, key:int) -> bool:
        if key in (K_w, K_UP): # top left
            x = self.current_tile.top_left

        elif key in (K_d, K_RIGHT): # top right
            x = self.current_tile.top_right

        elif key in (K_a, K_LEFT): # bottom left
            x = self.current_tile.bottom_left

        elif key in (K_s, K_DOWN): # bottom right
            x = self.current_tile.bottom_right

        elif key == K_RETURN:
            if self.selected_tile is not self.current_tile:
            # if self.selected_tile.tile_contents in TRAVERSABLE_TILE_CONTENT_TYPES:
                self.current_tile = self.selected_tile
                self.selected = False
                self.current_tile.traversed = True
                self.current_tile.show_surroundings()
                self.calculate_pos()
                return True
            return False
            # else:
            #     self.selected_tile = self.current_tile
            #     self.selected = False
            #     return False


        else:
            return False

        if (not x.is_stopper) and (x.tile_contents in TRAVERSABLE_TILE_CONTENT_TYPES) and(x.tile_type != 4):
            self.selected_tile = x
            self.selected = True

        return False