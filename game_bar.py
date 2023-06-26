import pygame
from pygame.locals import K_1, K_2, K_3, K_RETURN
from asset_handler import AssetHandler
from settings import GAME_BAR_WIDTH_HEIGHT, SCREEN_INIT_HEIGHT, SCREEN_INIT_WIDTH, BRAINS_COLLECTET_WIDTH, BRAINS_COLLECTET_HEIGHT, \
    MAX_LIFE, BLACK

class GameBar():
    def __init__(self, asset_handler:AssetHandler, brains_goal:int=10):
        self.asset_handler = asset_handler

        x = 0
        y = 0
        w = GAME_BAR_WIDTH_HEIGHT
        h = w

        # general
        self.home_button = pygame.Rect(x, y, w, h)
        x += 2 * w
        self.life_container = pygame.Rect(x, y, w, h)

        self.life = MAX_LIFE

        # brains
        self.current_brains = 0
        self.brains_goal = brains_goal
        self.brains_rects = list()
        self.create_brains_rects()

        # items
        x = self.brains_rects[-1].right + w
        self.brain_capture_rect = pygame.Rect(x, y, w, h)
        x += w + w / 2
        self.item_1_rect = pygame.Rect(x, y, w, h)
        x += w + w / 2
        self.item_2_rect = pygame.Rect(x, y, w, h)

        self.amount_brain_capture = 0
        self.item_1 = 4
        self.item_2 = 10
        self.selected_item = 0
        self.item_use = 8
        self.show_selected_item = True

        # move stuff
        x = SCREEN_INIT_WIDTH - w
        self.arrow_right = pygame.Rect(x, y, w, h)
        x -= w
        self.arrow_down = pygame.Rect(x, y, w, h)
        x -= w
        self.arrow_up = pygame.Rect(x, y, w, h)
        x -= w
        self.arrow_left = pygame.Rect(x, y, w, h)
        x -= w
        self.zoom_player = pygame.Rect(x, y, w, h)

        # choose item
        self.choose_weapon = False
        self.choose_weapon_text = self.asset_handler.FONT.render3(["2 to replace first item", "3 to replace second item", "ESC to discard weapon"])
        _x = SCREEN_INIT_WIDTH / 2 - self.choose_weapon_text.get_width() / 2
        _y = SCREEN_INIT_HEIGHT / 2 - self.choose_weapon_text.get_height() / 2
        self.choose_weapon_text_pos = (_x, _y)
        self.item_to_choose = 1
        _x = SCREEN_INIT_WIDTH / 2 - self.asset_handler.ITEMS[self.item_to_choose].get_width() / 2
        _y = _y - self.asset_handler.ITEMS[self.item_to_choose].get_height()
        self.item_to_choose_pos = (_x, _y)

        # create surface
        self.surf = None
        self.create_surf()

    def create_surf(self):
        s = pygame.Surface((SCREEN_INIT_WIDTH, GAME_BAR_WIDTH_HEIGHT))
        s.set_colorkey(BLACK)
        i = self.asset_handler.GAME_BAR

        s.blit(i[0], self.home_button.topleft)
        s.blit(i[15 - self.life], self.life_container.topleft)
        s.blit(i[5], self.life_container.topleft)

        if self.amount_brain_capture <= 0:
            s.blit(self.asset_handler.ITEMS[9], self.brain_capture_rect.topleft)
        else:
            s.blit(self.asset_handler.ITEMS[8], self.brain_capture_rect.topleft)
        s.blit(self.asset_handler.ITEMS[self.item_1], self.item_1_rect.topleft)
        s.blit(self.asset_handler.ITEMS[self.item_2], self.item_2_rect.topleft)

        if self.show_selected_item:
            if self.selected_item == 0:
                s.blit(self.asset_handler.ITEM_SELECTED, self.brain_capture_rect.topleft)
            elif self.selected_item == 1:
                s.blit(self.asset_handler.ITEM_SELECTED, self.item_1_rect.topleft)
            elif self.selected_item == 2:
                s.blit(self.asset_handler.ITEM_SELECTED, self.item_2_rect.topleft)

        t = self.asset_handler.FONT.render3([str(self.amount_brain_capture)])
        x = self.brain_capture_rect.x + self.brain_capture_rect.w / 2 - t.get_width() / 2
        y = self.brain_capture_rect.y + self.brain_capture_rect.h / 2 - t.get_height() / 2
        s.blit(t, (x, y))

        s.blit(i[16], self.zoom_player.topleft)
        s.blit(i[2], self.arrow_right.topleft)
        s.blit(i[3], self.arrow_down.topleft)
        s.blit(i[4], self.arrow_up.topleft)
        s.blit(i[1], self.arrow_left.topleft)

        temp = self.current_brains
        for i in range(0, self.brains_goal, 1):
            if temp > 0:
                s.blit(self.asset_handler.BRAINS_COLLECTED[1], self.brains_rects[i].topleft)
                temp -= 1
            else:
                s.blit(self.asset_handler.BRAINS_COLLECTED[0], self.brains_rects[i].topleft)

        self.surf = s

    def draw(self, surf:pygame.Surface):
        surf.blit(self.surf, (0, 0))

        if self.choose_weapon:
            surf.blit(self.asset_handler.ITEMS[self.item_to_choose], self.item_to_choose_pos)
            surf.blit(self.choose_weapon_text, self.choose_weapon_text_pos)

    def check_collisions(self, pos:tuple[int, int]) -> int:
        """
        -1 -> Nothing
        0 -> Home button
        1 -> Arrow left
        2 -> Arrow down
        3 -> Arrow up
        4 -> Arrow right
        5 -> Center on player
        6 -> Brain capture
        7 -> Item 1
        8 -> Item 2
        """
        if self.home_button.collidepoint(pos):
            self.show_selected_item = False
            self.create_surf()
            return 0
        elif self.arrow_left.collidepoint(pos):
            self.show_selected_item = False
            self.create_surf()
            return 1
        elif self.arrow_down.collidepoint(pos):
            self.show_selected_item = False
            self.create_surf()
            return 2
        elif self.arrow_up.collidepoint(pos):
            self.show_selected_item = False
            self.create_surf()
            return 3
        elif self.arrow_right.collidepoint(pos):
            self.show_selected_item = False
            self.create_surf()
            return 4
        elif self.zoom_player.collidepoint(pos):
            self.show_selected_item = False
            self.create_surf()
            return 5

        elif self.brain_capture_rect.collidepoint(pos):
            self.selected_item = 0
            self.item_use = 8
            self.show_selected_item = True
            self.create_surf()
            return 6
        elif self.item_1_rect.collidepoint(pos):
            self.selected_item = 1
            self.show_selected_item = True
            self.create_surf()
            return 7
        elif self.item_2_rect.collidepoint(pos):
            self.selected_item = 2
            self.show_selected_item = True
            self.create_surf()
            return 8
        else:
            self.show_selected_item = False
            self.create_surf()
            return -1

    def decrease_life(self, amount:int) -> bool:
        self.life -= amount

        if self.life <= 0:
            return True
        else:
            self.create_surf()
            return False

    def create_brains_rects(self):
        x = self.life_container.right + BRAINS_COLLECTET_WIDTH
        y = [0, BRAINS_COLLECTET_HEIGHT]
        w = BRAINS_COLLECTET_WIDTH
        h = BRAINS_COLLECTET_HEIGHT
        x_add = [0, w]

        for i in range(0, self.brains_goal, 1):
            self.brains_rects.append(pygame.Rect(x, y[0], w, h))
            y.reverse()
            x += x_add[0]

            x_add.reverse()

    def increase_collected_brains(self, amount:int) -> bool:
        self.current_brains += amount
        
        if self.current_brains >= self.brains_goal:
            return True
        else:
            self.create_surf()
            return False

    def on_key_press(self, key:int) -> bool:
        if key == K_1:
            self.selected_item = 0
            self.item_use = 8
            self.show_selected_item = True
            self.create_surf()
            return True
        elif key == K_2:
            self.selected_item = 1
            self.item_use = self.item_1
            self.show_selected_item = True
            self.create_surf()
            return True
        elif key == K_3:
            self.selected_item = 2
            self.item_use = self.item_2
            self.show_selected_item = True
            self.create_surf()
            return True
        
        elif key == K_RETURN:
            return True

        else:
            self.show_selected_item = False
            self.create_surf()
            return False

    def heal(self):
        self.life = MAX_LIFE
        self.create_surf()