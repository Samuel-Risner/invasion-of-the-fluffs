from random import choice

import pygame

from settings import CHEST_AVAILABLE_ITEMS
from tile import Tile
from asset_handler import AssetHandler
from player import Player
from game_bar import GameBar

def random_chest_item() -> int:
    return choice(CHEST_AVAILABLE_ITEMS)

def _get_tiles_n(tile:Tile) -> list[Tile]:
    to_return = list()

    p = [tile.top_left, tile.top_right, tile.bottom_left, tile.bottom_right]
    for i in p:
        if i.visible and (not i.is_stopper):
            to_return.append(i)

    return to_return

def _get_tiles_d(tile:Tile) -> list[Tile]:
    to_return = list()

    diagonal_tiles = set()
    x = tile.top_left
    if not x.is_stopper:
        diagonal_tiles.add(x.top_right)
        diagonal_tiles.add(x.bottom_left)
    x = tile.top_right
    if not x.is_stopper:
        diagonal_tiles.add(x.top_left)
        diagonal_tiles.add(x.bottom_right)
    x = tile.bottom_left
    if not x.is_stopper:
        diagonal_tiles.add(x.top_left)
        diagonal_tiles.add(x.bottom_right)
    x = tile.bottom_right
    if not x.is_stopper:
        diagonal_tiles.add(x.top_right)
        diagonal_tiles.add(x.bottom_left)

    for i in diagonal_tiles:
        if i.visible and (not i.is_stopper):
            to_return.append(i)

    return to_return

"""
0 -> Push tiles up, diagonal
1 -> Push tiles up, next to
2 -> Healing potion
3 -> Remove cooldown potion
4 -> Punch
5 -> Magic staff
6 -> Bow and arrow
7 -> Bow and flaming arrow
8 -> Brain capture
9 -> Empty brain capture
10 -> empty weapon slot
"""

class ItemsParent():

    def get_available_tiles(self, tile:Tile) -> int:
        return 0

    def draw(self, surf:pygame.Surface):
        pass

    def change_target(self):
        pass

    def do(self, in_game) -> int:
        return 0

class TilesD(ItemsParent):

    def __init__(self, asset_handler:AssetHandler, game_bar:GameBar):
        self.asset_handler = asset_handler
        self.game_bar = game_bar
        self.available_tiles = []

    def get_available_tiles(self, tile:Tile) -> int:
        self.available_tiles.clear()

        diagonal_tiles = set()

        x = tile.top_left
        if not x.is_stopper:
            diagonal_tiles.add(x.top_right)
            diagonal_tiles.add(x.bottom_left)
        x = tile.top_right
        if not x.is_stopper:
            diagonal_tiles.add(x.top_left)
            diagonal_tiles.add(x.bottom_right)
        x = tile.bottom_left
        if not x.is_stopper:
            diagonal_tiles.add(x.top_left)
            diagonal_tiles.add(x.bottom_right)
        x = tile.bottom_right
        if not x.is_stopper:
            diagonal_tiles.add(x.top_right)
            diagonal_tiles.add(x.bottom_left)

        for i in diagonal_tiles:
            if i.visible and (i.tile_contents not in (3, 7)) and (not i.is_stopper):
                self.available_tiles.append(i)

        if len(self.available_tiles) == 0:
            return 0

        return 1

    def draw(self, surf:pygame.Surface):
        for i in self.available_tiles:
            surf.blit(self.asset_handler.HIGHLIGHTS[2], i.rect.topleft)

    def change_target(self):
        return

    def do(self, in_game) -> int:
        for i in self.available_tiles:
            i.tile_contents = -1
            i.create_surf()
        
        in_game.check_fluff()
        return 0

class TilesN(ItemsParent):
    def __init__(self, asset_handler:AssetHandler, game_bar:GameBar):
        self.asset_handler = asset_handler
        self.game_bar = game_bar
        self.available_tiles = []

    def get_available_tiles(self, tile:Tile) -> int:
        self.available_tiles.clear()
        p = [tile.top_left, tile.top_right, tile.bottom_left, tile.bottom_right]
        for i in p:
            if i.visible and (i.tile_contents not in (3, 7)) and (not i.is_stopper):
                self.available_tiles.append(i)

        return 1

    def draw(self, surf:pygame.Surface):
        for i in self.available_tiles:
            surf.blit(self.asset_handler.HIGHLIGHTS[2], i.rect.topleft)

    def change_target(self):
        return

    def do(self, in_game) -> int:
        for i in self.available_tiles:
            i.tile_contents = -1
            i.create_surf()
        
        in_game.check_fluff()
        return 0

class Heal(ItemsParent):

    def __init__(self, asset_handler:AssetHandler, game_bar:GameBar):
        self.asset_handler = asset_handler
        self.game_bar = game_bar
        self.available_tiles = None

    def get_available_tiles(self, tile:Tile) -> int:
        self.available_tiles = tile
        return 1

    def draw(self, surf:pygame.Surface):
        if self.available_tiles != None:
            surf.blit(self.asset_handler.HIGHLIGHTS[2], self.available_tiles.rect.topleft)

    def change_target(self):
        return

    def do(self, in_game) -> int:
        self.game_bar.heal()
        return 0

class RemoveCooldown(ItemsParent):
    pass

class Punch(ItemsParent):
    def __init__(self, asset_handler:AssetHandler, game_bar:GameBar):
        self.asset_handler = asset_handler
        self.game_bar = game_bar
        self.available_tiles = list()
        self.selected = 0

    def get_available_tiles(self, tile:Tile) -> int:
        self.available_tiles.clear()
        self.selected = 0

        p = (tile, tile.top_left, tile.top_right, tile.bottom_left, tile.bottom_right)

        for i in p:
            if (i.tile_contents == 4) and (i.visible):
                self.available_tiles.append(i)
        
        if len(self.available_tiles) != 0:
            return 1

        return 0

    def draw(self, surf:pygame.Surface):
        for i in range(0, len(self.available_tiles), 1):
            t = self.available_tiles[i]
            if i == self.selected:
                surf.blit(self.asset_handler.HIGHLIGHTS[2], t.rect.topleft)
            else:
                surf.blit(self.asset_handler.HIGHLIGHTS[1], t.rect.topleft)

    def change_target(self):
        self.selected += 1
        if self.selected >= len(self.available_tiles):
            self.selected = 0

    def do(self, in_game) -> int:
        t = self.available_tiles[self.selected]
        t.tile_contents = -1
        t.create_surf()
        in_game.check_fluff()
        return 0

class MagicStaff(ItemsParent):

    def __init__(self, asset_handler:AssetHandler, game_bar:GameBar):
        self.asset_handler = asset_handler
        self.game_bar = game_bar
        self.available_tiles = list()
        self.selected = 0

    def get_available_tiles(self, tile:Tile) -> int:
        self.available_tiles.clear()
        self.selected = 0

        p1 = _get_tiles_d(tile)
        p2 = _get_tiles_n(tile)
        p3 = list()
        p3.extend(p1)
        p3.extend(p2)

        p4 = list()
        for i in p3:
            if (not i.is_stopper) and (i.visible):
                p4.extend(_get_tiles_d(i))
                p4.extend(_get_tiles_n(i))

        total = set()
        for i in p4:
            if i.tile_contents in (4, 1):
                total.add(i)

        for i in total:
            self.available_tiles.append(i)

        if len(self.available_tiles) == 0:
            return 0

        return 1

    def draw(self, surf:pygame.Surface):
        for i in range(0, len(self.available_tiles), 1):
            x = 1
            if i == self.selected:
                x = 2

            surf.blit(self.asset_handler.HIGHLIGHTS[x], self.available_tiles[i].rect.topleft)

    def change_target(self):
        self.selected += 1
        if self.selected >= len(self.available_tiles):
            self.selected = 0

    def do(self, in_game) -> int:
        t = self.available_tiles[self.selected]
        c = t.tile_contents
        t.tile_contents = -1
        t.create_surf()

        if c == 4:
            in_game.check_fluff()

        return 0

class Bow(ItemsParent):
    def __init__(self, asset_handler:AssetHandler, game_bar:GameBar):
        self.asset_handler = asset_handler
        self.game_bar = game_bar
        self.available_tiles = list()
        self.selected = 0

    def get_available_tiles(self, tile:Tile) -> int:
        self.available_tiles.clear()
        self.selected = 0

        p1 = _get_tiles_d(tile)
        p2 = _get_tiles_n(tile)
        p3 = list()
        p3.extend(p1)
        p3.extend(p2)

        p4 = list()
        for i in p3:
            if (not i.is_stopper) and (i.visible):
                p4.extend(_get_tiles_d(i))
                p4.extend(_get_tiles_n(i))

        p5 = list()
        for i in p4:
            if (not i.is_stopper) and (i.visible):
                p5.extend(_get_tiles_d(i))
                p5.extend(_get_tiles_n(i))

        total = set()
        for i in p5:
            if i.tile_contents == 4:
                total.add(i)

        for i in total:
            self.available_tiles.append(i)

        if len(self.available_tiles) == 0:
            return 0

        return 1

    def draw(self, surf:pygame.Surface):
        for i in range(0, len(self.available_tiles), 1):
            x = 1
            if i == self.selected:
                x = 2

            surf.blit(self.asset_handler.HIGHLIGHTS[x], self.available_tiles[i].rect.topleft)

    def change_target(self):
        self.selected += 1
        if self.selected >= len(self.available_tiles):
            self.selected = 0

    def do(self, in_game) -> int:
        t = self.available_tiles[self.selected]
        c = t.tile_contents
        t.tile_contents = -1
        t.create_surf()

        if c == 4:
            in_game.check_fluff()

        return 0

class BowF(ItemsParent):
    def __init__(self, asset_handler:AssetHandler, game_bar:GameBar):
        self.asset_handler = asset_handler
        self.game_bar = game_bar
        self.available_tiles = list()
        self.selected = 0

    def get_available_tiles(self, tile:Tile) -> int:
        self.available_tiles.clear()
        self.selected = 0

        p1 = _get_tiles_d(tile)
        p2 = _get_tiles_n(tile)
        p3 = list()
        p3.extend(p1)
        p3.extend(p2)

        p4 = list()
        for i in p3:
            if (not i.is_stopper) and (i.visible):
                p4.extend(_get_tiles_d(i))
                p4.extend(_get_tiles_n(i))

        p5 = list()
        for i in p4:
            if (not i.is_stopper) and (i.visible):
                p5.extend(_get_tiles_d(i))
                p5.extend(_get_tiles_n(i))

        total = set()
        for i in p5:
            if i.tile_contents in (4, 0):
                total.add(i)

        for i in total:
            self.available_tiles.append(i)

        if len(self.available_tiles) == 0:
            return 0

        return 1

    def draw(self, surf:pygame.Surface):
        for i in range(0, len(self.available_tiles), 1):
            x = 1
            if i == self.selected:
                x = 2

            surf.blit(self.asset_handler.HIGHLIGHTS[x], self.available_tiles[i].rect.topleft)

    def change_target(self):
        self.selected += 1
        if self.selected >= len(self.available_tiles):
            self.selected = 0

    def do(self, in_game) -> int:
        t = self.available_tiles[self.selected]
        c = t.tile_contents
        t.tile_contents = -1
        t.create_surf()

        if c == 4:
            in_game.check_fluff()

        return 0

class BrainCatcher(ItemsParent):

    def __init__(self, asset_handler:AssetHandler, game_bar:GameBar):
        self.asset_handler = asset_handler
        self.game_bar = game_bar
        self.available_tiles = []

        self.target = 0

        self.amount = 0

    def get_available_tiles(self, tile:Tile) -> int:
        # print("get")
        self.available_tiles.clear()

        if self.amount <= 0:
            return 0

        if tile.top_left.tile_contents == 3:
            self.available_tiles.append(tile.top_left)

        if tile.top_right.tile_contents == 3:
            self.available_tiles.append(tile.top_right)

        if tile.bottom_left.tile_contents == 3:
            self.available_tiles.append(tile.bottom_left)

        if tile.bottom_right.tile_contents == 3:
            self.available_tiles.append(tile.bottom_right)

        return 1

    def draw(self, surf:pygame.Surface):
        for i in range(0, len(self.available_tiles), 1):
            x = 1
            if i == self.target:
                x = 2
            surf.blit(self.asset_handler.HIGHLIGHTS[x], self.available_tiles[i].rect.topleft)

    def change_target(self):
        # print("change")
        self.target += 1
        if self.target >= len(self.available_tiles):
            self.target = 0

    def do(self, in_game) -> int:        
        self.amount -= 1
        self.game_bar.amount_brain_capture = self.amount

        if len(self.available_tiles) == 0:
            return
        # print("do")
        b = None
        for i in in_game.brains:
            if i.tile is self.available_tiles[self.target]:
                b = i
                break
        in_game.game_bar.increase_collected_brains(1)
        in_game.brains.remove(b)
        self.available_tiles[self.target].tile_contents = -1
        self.available_tiles[self.target].create_surf()

        return 0

def get_item_classes(asset_handler:AssetHandler, game_bar:GameBar):
    return [
        TilesD(asset_handler, game_bar),
        TilesN(asset_handler, game_bar),
        Heal(asset_handler, game_bar),
        RemoveCooldown(),
        Punch(asset_handler, game_bar),
        MagicStaff(asset_handler, game_bar),
        Bow(asset_handler, game_bar),
        BowF(asset_handler, game_bar),
        BrainCatcher(asset_handler, game_bar),
        ItemsParent(),
        ItemsParent()
    ]