import pygame

from settings import PINK, GREEN, CYAN, TILES_WIDTH, TILES_HEIGHT_SMALL, TILES_HEIGHT_LARGE, \
    PLAYER_WIDTH, PLAYER_HEIGHT, GAME_BAR_WIDTH_HEIGHT, BRAINS_COLLECTET_WIDTH, BRAINS_COLLECTET_HEIGHT, \
    TEXT_SKIP_W_H
from font import Font

class AssetHandler():

    def __init__(self):
        self.TILES_BARREN = self._load_spritesheet("assets/tiles/barren.png")
        self.TILES_GRASS = self._load_spritesheet("assets/tiles/grass.png")
        self.TILES_ROCK = self._load_spritesheet("assets/tiles/rock.png")
        self.TILES_WATER_SHALLOW = self._load_spritesheet("assets/tiles/water_shallow.png")
        self.TILES_WATER_SOLID = self._load_spritesheet("assets/tiles/water_solid.png")

        self.ALL_TILES = (
            self.TILES_BARREN,
            self.TILES_GRASS,
            self.TILES_ROCK,
            self.TILES_WATER_SHALLOW,
            self.TILES_WATER_SOLID
        )
        self._scale_tiles()
        # self._scale(self.ALL_TILES, TILES_WIDTH, TILES_HEIGHT_SMALL)

        self.TILE_CONTENTS = self._load_spritesheet("assets/tile_contents.png")
        # self._scale_tile_contents()
        self._scale(self.TILE_CONTENTS, TILES_WIDTH, TILES_HEIGHT_SMALL)

        self.PLAYER = pygame.transform.scale(
            pygame.image.load("assets/player.png"),
            (PLAYER_WIDTH, PLAYER_HEIGHT)
        )

        self.HIGHLIGHTS = self._load_spritesheet("assets/highlights.png")
        self._scale(self.HIGHLIGHTS, TILES_WIDTH, TILES_HEIGHT_SMALL)
        # pygame.transform.scale(
        #     pygame.image.load("assets/tile_highlight.png"),
        #     (TILES_WIDTH, TILES_HEIGHT_SMALL)
        # )

        self.GAME_BAR = self._load_spritesheet("assets/game_bar.png")
        """ Index:
        0 -> Home button
        1 -> Arrow left
        2 -> Arrow right
        3 -> Arrow down
        4 -> Arrow up
        5 -> Life container
        6 - 15 -> Life level 9x, the 10th one is empty
        16 -> Zoom back to player
        """
        # self._scale_game_bar()
        self._scale(self.GAME_BAR, GAME_BAR_WIDTH_HEIGHT, GAME_BAR_WIDTH_HEIGHT)

        self.FONT = Font()

        self.MOBS = self._load_spritesheet("assets/mobs.png")
        """Index:
        0 -> brain
        1 -> fluff
        """
        # self._scale_mobs()
        self._scale(self.MOBS, TILES_WIDTH, TILES_HEIGHT_SMALL)

        self.TILE_CONTENTS.extend(self.MOBS)

        self.BRAINS_COLLECTED = self._load_spritesheet("assets/wanted_brains.png")
        # self._scale_brains_collected()
        self._scale(self.BRAINS_COLLECTED, BRAINS_COLLECTET_WIDTH, BRAINS_COLLECTET_HEIGHT)

        self.ITEMS = self._load_spritesheet("assets/items.png")
        """Index:
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
        10 -> Empty slot
        """
        self._scale(self.ITEMS, GAME_BAR_WIDTH_HEIGHT, GAME_BAR_WIDTH_HEIGHT)

        self.ITEM_SELECTED = pygame.transform.scale(
            pygame.image.load("assets/item_selected.png"),
            (GAME_BAR_WIDTH_HEIGHT, GAME_BAR_WIDTH_HEIGHT)
        ).convert_alpha()

        self.INTERACTABLES = self._load_spritesheet("assets/interactables.png")
        self._scale(self.INTERACTABLES, TILES_WIDTH, TILES_HEIGHT_SMALL)
        self.TILE_CONTENTS.extend(self.INTERACTABLES)

        self.SKIP_TEXT = pygame.transform.scale(
            pygame.image.load("assets/skip_text_button.png"),
            (TEXT_SKIP_W_H, TEXT_SKIP_W_H)
        )

    def _load_spritesheet(self, path:str) -> list[pygame.Surface]:
        """Returns a list containing the individual sprites from the `path` file. No error handeling is done here 
        so make sure the sprite sheet matches the requirements (look at "assets/tiles/)."""

        """The cut out images that are to be returned"""
        to_return   = []
        """Y-Coordinates for the top (left) of the individual sprites, X is assumed to be 0."""
        rows_top    = []
        """Y-Coordinates for the bottom (left) of the individual sprites, X is assumed to be 0."""
        rows_bottom = []
        """Y- and X-Coordinates for the bottom right of the individual sprites.."""
        rows_end    = []
        """Are used to cut out the individual sprites from the sheet."""
        rects       = []
        
        """The colour which signalises the top (left) of the individual sorites."""
        top         = PINK
        """The colour which signalises the bottom (left) of the individual sorites."""
        bottom      = CYAN
        """The colour which signalises zhe bottom right of the individual sorites."""
        end         = GREEN
        
        """The sprite sheet containing the individual sprites."""
        img = pygame.image.load(path)
        
        """The width of the sprite sheet."""
        max_w = img.get_width()
        """The height of the sprite sheet."""
        max_h = img.get_height()
        
        """Getting the Y-Coordinates for the `rows_top` and `rows_bottom` lists."""
        for y in range(0, max_h, 1):
            colour = img.get_at((0, y))
            if colour == top:
                rows_top.append(y)
            elif colour == bottom:
                rows_bottom.append(y)

        """Getting the X- and Y-Coordinates for the `rows_end` list."""
        for y in rows_bottom:
            for x in range(0, max_w, 1):
                if img.get_at((x, y)) == end:
                    rows_end.append((x, y))
                    break
        
        """Populating the `rects` list with the already aquired coordinates and values."""
        for i in range(0, len(rows_end), 1):
            r = pygame.Rect(0, 0, 0, 0)
            r.x = 1
            r.y = rows_top[i] + 1
            r.w = rows_end[i][0] - 1
            r.h = rows_bottom[i] - rows_top[i] - 1

            rects.append(r)

        """Cutting out the individual sprites from the sprite sheet using the `rect` list and saving them in the
        'to_return' list."""
        for i in rects:
            _img = img.copy()
            _img.set_clip(i)
            _img = img.subsurface(_img.get_clip())

            to_return.append(_img.convert_alpha())

        """Duh."""
        return to_return

    def _scale(self, _list:list, w:int, h:int):
        for i in range(0, len(_list), 1):
            _list[i] = pygame.transform.scale(
                _list[i],
                (w, h)
            ).convert_alpha()

    def _scale_tiles(self):
        """Scales the tile images up and converts them."""

        for tile_set in self.ALL_TILES:

            """The first three tiles have `TILES_HEIGHT_LARGE`, the last one doesn't."""

            for tile in range(0, 3, 1):
                tile_set[tile] = pygame.transform.scale(
                    tile_set[tile],
                    (TILES_WIDTH, TILES_HEIGHT_LARGE)
                ).convert_alpha()

            tile_set[-1] = pygame.transform.scale(
                    tile_set[-1],
                    (TILES_WIDTH, TILES_HEIGHT_SMALL)
                ).convert_alpha()

    def _scale_tile_contents(self):
        """Scales the sub tile content images up and converts them."""

        for i in range(0, len(self.TILE_CONTENTS), 1):
            self.TILE_CONTENTS[i] = pygame.transform.scale(
                self.TILE_CONTENTS[i],
                (TILES_WIDTH, TILES_HEIGHT_SMALL)
            ).convert_alpha()

    def _scale_game_bar(self):
        for i in range(0, len(self.GAME_BAR), 1):
            self.GAME_BAR[i] = pygame.transform.scale(
                self.GAME_BAR[i],
                (GAME_BAR_WIDTH_HEIGHT, GAME_BAR_WIDTH_HEIGHT)
            ).convert_alpha()

    def _scale_mobs(self):
        for i in range(0, len(self.MOBS), 1):
            self.MOBS[i] = pygame.transform.scale(
                self.MOBS[i],
                (TILES_WIDTH, TILES_HEIGHT_SMALL)
            ).convert_alpha()

    def _scale_brains_collected(self):
        for i in range(0, len(self.BRAINS_COLLECTED), 1):
            self.BRAINS_COLLECTED[i] = pygame.transform.scale(
                self.BRAINS_COLLECTED[i],
                (BRAINS_COLLECTET_WIDTH, BRAINS_COLLECTET_HEIGHT)
            ).convert_alpha()