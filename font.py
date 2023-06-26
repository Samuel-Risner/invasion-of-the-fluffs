import pygame

from settings import BLACK, PINK, FONT_SCALE, SPACE_LETTERS, SPACE_LINES, FONT_BACKGROUND, FONT_COLOUR

class Font():

    def __init__(self):
        self.font_order = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R",
        "S", "T", "U", "V", "W", "X", "Y", "Z", ".", "!", ",", "?", "a", "b", "c", "d", "e", "f", "g", "h", "i",
        "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4",
        "5", "6", "7", "8", "9", "0", " "]

        self.font_order_2 = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R",
        "S", "T", "U", "V", "W", "X", "Y", "Z", ".", "!", ",", "?", "0", "1", "2", "3", "4",
        "5", "6", "7", "8", "9", " "]

        self.small_letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

        self.letters = list()

        self._load()

    def clip(self, surf:pygame.Surface, x:int, y:int, w:int, h:int) -> pygame.Surface:
        """Gets a cutout from `surf` at positions `x` and `y` with the specified width `w` and height `h`. """
        handle_surf = surf.copy()
        clip_rect = pygame.Rect(x, y, w, h)
        handle_surf.set_clip(clip_rect)
        image = surf.subsurface(handle_surf.get_clip())

        return pygame.transform.scale(
            image,
            (image.get_width() * FONT_SCALE, image.get_height() * FONT_SCALE)
        ).convert_alpha()
        
        # return image.copy().convert_alpha()

    def _load(self):
        img = pygame.image.load("assets/font3.png")

        _x = 0
        y = 0
        w = img.get_width()
        h = img.get_height()

        for x in range(0, w, 1):
            if img.get_at((x, y)) == PINK:
                _w = x - _x
                temp = self.clip(img, _x, y, _w, h)
                temp = pygame.transform.scale(temp, (temp.get_width() / 2, temp.get_height() / 2))
                self.letters.append(temp)
                _x = x + 1
                

    def render(self, text:list[str]) -> pygame.Surface:
        lines = list()

        for line in text:
            lines.append(list())
            for letter in line:
                x = self.font_order.index(letter)
                x = self.letters[x]
                lines[-1].append(x)

        widths = list()
        for line in lines:
            widths.append(0)

            for letter in line:
                widths[-1] += letter.get_width() + SPACE_LETTERS

            widths[-1] -= SPACE_LETTERS

        largest_width = widths[0]
        for w in widths:
            if w > largest_width:
                largest_width = w
        
        total_height = lines[0][0].get_height() * len(lines) + (len(lines) - 1) * SPACE_LINES

        s = pygame.Surface((largest_width, total_height))
        s.fill(FONT_BACKGROUND)

        x = 0
        y = 0

        for line in lines:
            for letter in line:
                s.blit(letter, (x, y))
                x += letter.get_width()
                x += SPACE_LETTERS
            
            x = 0
            y += lines[0][0].get_height()
            y += SPACE_LINES

        s = s.convert()

        return s

    def p_alette_swap(self, surf, old_c, new_c):
        img_copy = pygame.Surface(surf.get_size())
        img_copy.fill(new_c)
        surf.set_colorkey(old_c)
        img_copy.blit(surf, (0, 0))
        return img_copy

    def render2(self, text:list[str]) -> pygame.Surface:
        lines = list()

        for line in text:
            lines.append(list())
            for letter in line:
                x = self.font_order.index(letter)
                x = self.letters[x]
                lines[-1].append(x)

        widths = list()
        for line in lines:
            widths.append(0)

            for letter in line:
                widths[-1] += letter.get_width() + SPACE_LETTERS

            widths[-1] -= SPACE_LETTERS

        largest_width = widths[0]
        for w in widths:
            if w > largest_width:
                largest_width = w
        
        total_height = lines[0][0].get_height() * len(lines) + (len(lines) - 1) * SPACE_LINES

        s = pygame.Surface((largest_width, total_height))
        s.fill(FONT_BACKGROUND)

        x = 0
        y = 0

        for line in lines:
            for letter in line:
                s.blit(letter, (x, y))
                x += letter.get_width()
                x += SPACE_LETTERS
            
            x = 0
            y += lines[0][0].get_height()
            y += SPACE_LINES

        s = self.p_alette_swap(s, BLACK, FONT_COLOUR)
        s.set_colorkey(FONT_BACKGROUND)

        s = s.convert_alpha()



        return s

    def render3(self, text:list[str]) -> pygame.Surface:
        lines = list()

        for line in text:
            lines.append(list())
            for letter in line:
                # print(letter)
                if letter in self.small_letters:
                    letter = self.font_order_2[self.small_letters.index(letter)]
                # print(letter)
                x = self.font_order_2.index(letter)
                # print(x)
                x = self.letters[x]
                lines[-1].append(x)

        widths = list()
        for line in lines:
            widths.append(0)

            for letter in line:
                widths[-1] += letter.get_width() + SPACE_LETTERS

            widths[-1] -= SPACE_LETTERS

        largest_width = widths[0]
        for w in widths:
            if w > largest_width:
                largest_width = w
        
        total_height = lines[0][0].get_height() * len(lines) + (len(lines) - 1) * SPACE_LINES

        s = pygame.Surface((largest_width, total_height))
        # s.fill(FONT_BACKGROUND)

        x = 0
        y = 0

        for line in lines:
            for letter in line:
                s.blit(letter, (x, y))
                x += letter.get_width()
                x += SPACE_LETTERS
            
            x = 0
            y += lines[0][0].get_height()
            y += SPACE_LINES

        # s = s.convert()
        s.set_colorkey(BLACK)
        s = s.convert_alpha()
        return s
