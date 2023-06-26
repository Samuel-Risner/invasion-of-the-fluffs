import pygame
from pygame import QUIT, VIDEORESIZE, RESIZABLE, KEYDOWN, KSCAN_F11, K_F11, FULLSCREEN, MOUSEBUTTONUP, K_ESCAPE

from settings import SCREEN_MIN_WIDTH, SCREEN_MIN_HEIGHT, FPS, BLACK, TILES_HEIGHT_SMALL, TILES_WIDTH
from data import Data
from map import load_map
from player import Player
from tile import Tile
from game_bar import GameBar

class InGame():

    def start(self, map_name:str, data:Data) -> bool:
        map, spawn, brains, fluffs, chests, relics = load_map(map_name, data.asset_handler)
        player = Player(data.asset_handler, spawn)
        game_bar = GameBar(data.asset_handler)

        # text = data.asset_handler.FONT.render(["AA", "Erste Zeile", "Zweite", "3."])

        self._center_tiles(map, player.current_tile, data, player)

        while True:
            data.CLOCK.tick(FPS)

            for event in pygame.event.get():
                if event.type == QUIT:
                    return True

                if event.type == VIDEORESIZE:
                    if not data.fullscreen:
                        data.screen_width, data.screen_height = event.w, event.h

                        if data.screen_width < SCREEN_MIN_WIDTH:
                            data.screen_width = SCREEN_MIN_WIDTH
                        if data.screen_height < SCREEN_MIN_HEIGHT:
                            data.screen_height = SCREEN_MIN_HEIGHT

                        data.screen = pygame.display.set_mode(
                            (data.screen_width, data.screen_height),
                            RESIZABLE
                        )

                        data.on_size_change()

                if event.type == KEYDOWN:

                    if event.key in (KSCAN_F11, K_F11):
                        data.fullscreen = not data.fullscreen

                        if data.fullscreen:
                            data.screen = pygame.display.set_mode(data.monitor_size, FULLSCREEN)
                            data.on_size_change()
                        else:
                            data.screen = pygame.display.set_mode(
                                (data.screen_width, data.screen_height),
                                RESIZABLE
                            )
                    else:
                        if game_bar.choose_weapon:
                            # game_bar
                            pass

                        elif game_bar.show_selected_item:
                            if game_bar.on_key_press(event.key):
                                    player.undo_selected()

                            if event.key == K_ESCAPE:
                                game_bar.show_selected_item = False
                                game_bar.create_surf()
                            else:
                                player.undo_selected()
                        else:
                            if player.on_key_press(event.key):
                                for i in fluffs:
                                    i.move()

                                for f in fluffs:
                                    if f.tile is player.current_tile:
                                        if game_bar.decrease_life(1):
                                            return False
                                    
                                    for b in brains:
                                        if b.tile is f.tile:
                                            return False
                                
                                for b in brains:
                                    if b.tile is player.current_tile:
                                        game_bar.increase_collected_brains(1)
                                        brains.remove(b)
                                        b.tile.tile_contents = -1
                                        b.tile.create_surf()
                                        break

                                for r in relics:
                                    if r.tile is player.current_tile:
                                        # print("r")
                                        player.current_tile.tile_contents = -1
                                        player.current_tile.create_surf()
                                        game_bar.amount_brain_capture += 1
                                        game_bar.create_surf()
                                
                                for c in chests:
                                    if c.tile is player.current_tile:
                                        # print("c")
                                        player.current_tile.tile_contents = -1
                                        player.current_tile.create_surf()
                                        game_bar.choose_weapon = True
                            else:
                                if game_bar.on_key_press(event.key):
                                    player.undo_selected()

                if event.type == MOUSEBUTTONUP:
                    if pygame.mouse.get_focused():
                        pos = data.get_mouse_pos()
                        x = game_bar.check_collisions(pos)
                        if x != -1:
                            if x == 0:
                                return False
                            elif x == 1:
                                self._move_tiles(TILES_WIDTH, 0, map, player)
                            elif x == 2:
                                self._move_tiles(0, TILES_HEIGHT_SMALL, map, player)
                            elif x == 3:
                                self._move_tiles(0, - TILES_HEIGHT_SMALL, map, player)
                            elif x == 4:
                                self._move_tiles(- TILES_WIDTH, 0, map, player)
                            elif x == 5:
                                self._center_tiles(map, player.current_tile, data, player)
                            elif x >= 6:
                                player.undo_selected()

            data.CANVAS.fill(BLACK)

            for i in map:
                i.draw(data.CANVAS)
            # for i in brains:
            #     i.draw(data.CANVAS)
            # for i in fluffs:
            #     i.draw(data.CANVAS)
            # for i in chests:
            #     i.draw(data.CANVAS)
            # for i in relics:
            #     i.draw(data.CANVAS)

            player.draw(data.CANVAS)
            game_bar.draw(data.CANVAS)

            # data.CANVAS.blit(text, (100, 100))

            data.screen.blit(
                pygame.transform.scale(
                    data.CANVAS, data.canvas_scale
                ).convert_alpha(), data.canvas_pos)

            pygame.display.update()

    def _center_tiles(self, tiles:list[Tile], center:Tile, data:Data, player:Player):
        """self._center_tiles(map, player.current_tile, data, player)"""
        center_x = data.canvas_scale[0] / 2 - center.rect.w / 2
        center_y = data.canvas_scale[1] / 2 - center.rect.h / 2

        x_move = center.rect.x - center_x
        y_move = center.rect.y - center_y

        for i in tiles:
            i.rect.x -= x_move
            i.rect.y -= y_move

        player.calculate_pos()

    def _move_tiles(self, x_add:int, y_add:int, tiles:list[Tile], player:Player):
        for i in tiles:
            i.rect.x += x_add
            i.rect.y += y_add

        player.calculate_pos()

    def save(self):
        pass

    def reset(self):
        pass