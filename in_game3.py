import pygame
from pygame import K_LSHIFT, K_RETURN, K_RSHIFT, QUIT, VIDEORESIZE, RESIZABLE, KEYDOWN, KSCAN_F11, K_F11, FULLSCREEN, MOUSEBUTTONUP, K_ESCAPE, \
    K_2, K_3

from settings import SCREEN_INIT_HEIGHT, SCREEN_INIT_WIDTH, SCREEN_MIN_WIDTH, SCREEN_MIN_HEIGHT, FPS, BLACK, TILES_HEIGHT_SMALL, TILES_WIDTH
from data import Data
from map import load_map
from player import Player
from tile import Tile
from game_bar import GameBar
from items import random_chest_item, get_item_classes
from story import Story

class InGame():

    def __init__(self, data:Data, map_name:str):
        self.data = data

        self.tiles, self.spawn, self.brains, self.fluffs, self.chests, self.relics = load_map(map_name, data.asset_handler)
        self.player = Player(data.asset_handler, self.spawn)
        self.game_bar = GameBar(data.asset_handler)
        self.story = Story(data.asset_handler)

        self._center_tiles(self.player.current_tile)

        self.item_classes = get_item_classes(data.asset_handler, self.game_bar)
        self.show_item_selection = False
        self.item_stage = 0
        self.using_item = False

    def start(self) -> int:
        """0 -> X pressed, 1 -> home button, 2 -> player eaten by fluff, 3 -> brain eaten by fluff"""

        CLOCK = pygame.time.Clock()
        while True:
            CLOCK.tick(60)

            for event in pygame.event.get():
                if event.type == QUIT:
                    return 0

                if event.type == VIDEORESIZE:
                    if not self.data.fullscreen:
                        self.data.screen_width, self.data.screen_height = event.w, event.h

                        if self.data.screen_width < SCREEN_MIN_WIDTH:
                            self.data.screen_width = SCREEN_MIN_WIDTH
                        if self.data.screen_height < SCREEN_MIN_HEIGHT:
                            self.data.screen_height = SCREEN_MIN_HEIGHT

                        self.data.screen = pygame.display.set_mode(
                            (self.data.screen_width, self.data.screen_height),
                            RESIZABLE
                        )

                        self.data.on_size_change()

                if event.type == KEYDOWN:

                    if event.key in (KSCAN_F11, K_F11):
                        self.data.fullscreen = not self.data.fullscreen

                        if self.data.fullscreen:
                            self.data.screen = pygame.display.set_mode(self.data.monitor_size, FULLSCREEN)
                            self.data.on_size_change()
                        else:
                            self.data.screen = pygame.display.set_mode(
                                (self.data.screen_width, self.data.screen_height),
                                RESIZABLE
                            )

                    else:
                        x = self._on_key(event.key)
                        if x != -1:
                            return x

                if event.type == MOUSEBUTTONUP:
                    if pygame.mouse.get_focused():
                        pos = self.data.get_mouse_pos()
                        x = self._on_click(pos)
                        if x != -1:
                            return x

            if self.game_bar.current_brains == self.game_bar.brains_goal:
                return 4

            self.data.CANVAS.fill(BLACK)

            for i in self.tiles:
                i.draw(self.data.CANVAS)

            self.player.draw(self.data.CANVAS)

            if self.using_item:
                self.item_classes[self.game_bar.item_use].draw(self.data.CANVAS)

            self.game_bar.draw(self.data.CANVAS)
            self.story.draw(self.data.CANVAS)

            self.data.screen.blit(
                pygame.transform.scale(
                    self.data.CANVAS, self.data.canvas_scale
                ).convert_alpha(), self.data.canvas_pos)

            pygame.display.update()

    def _center_tiles(self, center:Tile):
        """self._center_tiles(map, player.current_tile, data, player)"""
        # center_x = self.data.canvas_scale[0] / 2 - center.rect.w / 2
        # center_y = self.data.canvas_scale[1] / 2 - center.rect.h / 2
        center_x = SCREEN_INIT_WIDTH / 2 - center.rect.w / 2
        center_y = SCREEN_INIT_HEIGHT / 2 - center.rect.h / 2

        x_move = center.rect.x - center_x
        y_move = center.rect.y - center_y

        for i in self.tiles:
            i.rect.x -= x_move
            i.rect.y -= y_move

        self.player.calculate_pos()

    def _move_tiles(self, x_add:int, y_add:int):
        for i in self.tiles:
            i.rect.x += x_add
            i.rect.y += y_add

        self.player.calculate_pos()

    def _on_key(self, key:int) -> int:
        self.show_item_selection = False
        keys = pygame.key.get_pressed()

        if self.using_item:
            if self.item_stage == 0:
                self.using_item = False
                return -1

            i = self.game_bar.item_use

            if (keys[K_LSHIFT] or keys[K_RSHIFT]) and keys[K_RETURN]:
                self.item_stage = self.item_classes[i].do(self)
                self.using_item = False
            # elif (self.item_stage == 0) and (key not in (K_LSHIFT, K_RSHIFT)):
            #     self.item_classes[i].get_available_tiles(self.player.current_tile)
            #     self.item_stage += 1
            elif key == K_ESCAPE:
                self.item_stage = 0
                self.using_item = False
            elif (self.item_stage == 1) and (key not in (K_LSHIFT, K_RSHIFT)):
                self.item_classes[i].change_target()
                
        # Choose an item from an opened chest
        elif self.game_bar.choose_weapon:
            self.show_item_selection = False

            if key == K_ESCAPE:
                self.game_bar.choose_weapon = False

            elif key == K_2:
                self.game_bar.choose_weapon = False
                self.game_bar.item_1 = self.game_bar.item_to_choose
                self.game_bar.create_surf()

            elif key == K_3:
                self.game_bar.choose_weapon = False
                self.game_bar.item_2 = self.game_bar.item_to_choose
                self.game_bar.create_surf()

        elif self.game_bar.show_selected_item:
            k = pygame.key.get_pressed()
            if self.game_bar.on_key_press(key):
                self.player.undo_selected()
                self.show_item_selection = True

            if key == K_RETURN:
                self.using_item = True
                i = self.game_bar.item_use
                self.item_stage = self.item_classes[i].get_available_tiles(self.player.current_tile)
                

            elif key == K_ESCAPE:
                self.game_bar.show_selected_item = False
                self.game_bar.create_surf()

            else:
                self.player.undo_selected()

        else:
            self.show_item_selection = False

            if self.player.on_key_press(key):
                # print(self.player.current_tile.tile_contents)
                
                for i in self.fluffs:
                    if i.move():
                        return 3
                t = self.player.current_tile.tile_contents

                if t == 4:# fluff

                    if self.game_bar.decrease_life(1):
                        return 2
                    
                    # for b in self.brains:
                    #     if b.tile is f.tile:
                    #         return 3
                
                if t == 3: # brain
                    self.game_bar.increase_collected_brains(1)
                    # self.brains.remove(b)
                    self.player.current_tile.tile_contents = -1
                    self.player.current_tile.create_surf()
                    # break

                if t == 6: # relics

                # for r in self.relics:
                #     if r.tile is self.player.current_tile:
                    self.player.current_tile.tile_contents = -1
                    self.player.current_tile.create_surf()
                    self.game_bar.amount_brain_capture += 1
                    self.game_bar.create_surf()
                    self.item_classes[8].amount += 1
                    # self.relics.remove(r)
                    # break
                
                if t == 5: # chests
                # for c in self.chests:
                #     if c.tile is self.player.current_tile:
                    self.player.current_tile.tile_contents = -1
                    self.player.current_tile.create_surf()
                    self.game_bar.item_to_choose = random_chest_item()
                    self.game_bar.choose_weapon = True
                    # self.chests.remove(c)
                    # break

                if t == 7: # story
                    self.player.current_tile.tile_contents = 8
                    self.player.current_tile.create_surf()
                    # print(self.player.current_tile.story)
                    self.story.set_stage(self.player.current_tile.story)

            else:
                if self.game_bar.on_key_press(key):
                    self.player.undo_selected()

        return -1

    def _on_click(self, pos:tuple[int, int]) -> int:
        x = self.game_bar.check_collisions(pos)
        if x != -1:
            if x == 0:
                return 1
            elif x == 1:
                self._move_tiles(TILES_WIDTH, 0)
            elif x == 2:
                self._move_tiles(0, TILES_HEIGHT_SMALL)
            elif x == 3:
                self._move_tiles(0, - TILES_HEIGHT_SMALL)
            elif x == 4:
                self._move_tiles(- TILES_WIDTH, 0)
            elif x == 5:
                self._center_tiles(self.player.current_tile)
            elif x >= 6:
                self.player.undo_selected()

        self.story.on_click(pos)

        return -1

    def save(self):
        pass

    def reset(self):
        pass

    def check_fluff(self):
        to_remove = list()
        for i in self.fluffs:
            if i.tile.tile_contents != 4:
                to_remove.append(i)

        for i in to_remove:
            self.fluffs.remove(i)