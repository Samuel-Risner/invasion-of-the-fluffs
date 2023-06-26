import random

import pygame

from tile import Tile
from asset_handler import AssetHandler

class Parent():

    def __init__(self, tile:Tile, asset_handler:AssetHandler):
        self.tile = tile
        self.asset_handler = asset_handler

    def is_visible(self) -> bool:
        return self.tile.visible

class Brain(Parent):

    def __init__(self, tile:Tile, asset_handler:AssetHandler):
        super().__init__(tile, asset_handler)

class Fluff(Parent):

    def __init__(self, tile:Tile, asset_handler:AssetHandler):
        super().__init__(tile, asset_handler)

    def move(self) -> bool:
        def _move(tile:Tile) -> bool:
            if (tile.visible) and (not tile.is_stopper) and ((tile.traversable) or (tile.tile_contents == 3)) and (tile.tile_contents not in (7, 8)):
                self.tile.tile_contents = -1
                self.tile.create_surf()
                self.tile.update_traversable()

                b = False
                if tile.tile_contents == 3:
                    b = True

                tile.tile_contents = 4
                tile.create_surf()
                tile.update_traversable()

                self.tile = tile

                return b
            return False

        if not self.tile.visible:
            return False

        x = random.randint(0, 3)

        if x == 0:
            return _move(self.tile.top_left)
        elif x == 1:
            return _move(self.tile.top_right)
        elif x == 2:
            return _move(self.tile.bottom_left)
        elif x == 3:
            return _move(self.tile.bottom_right)

class Chest(Parent):

    def __init__(self, tile:Tile, asset_handler:AssetHandler):
        super().__init__(tile, asset_handler)

class Relic(Parent):

    def __init__(self, tile:Tile, asset_handler:AssetHandler):
        super().__init__(tile, asset_handler)
