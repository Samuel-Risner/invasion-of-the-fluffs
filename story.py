import pygame

from asset_handler import AssetHandler
from settings import SCREEN_INIT_HEIGHT, TEXT_SKIP_W_H

class Story():
    
    def __init__(self, asset_handler:AssetHandler):
        self.asset_handler = asset_handler

        self.stage = 0
        self.texts = list()
        self.pos = (0, 0)
        self.visible = False
        self.skip_rect = pygame.Rect(0, 0, TEXT_SKIP_W_H, TEXT_SKIP_W_H)

        self._load()
        # self.progress()

    def _load(self):
        text = [
            ["Welcome adventure person!", "Use 2 and 3 to defend yourself!", "ENTER to aquire targets and to", "switch between them.", "Pressing SHIFT plus ENTER", "will destroy them!"],
            ["Now, you may be wondering", "what you are doing here...", "The answer is simple", "The fluffs have invaded your home", "and have stolen all your friends brains", "your job is to save them", "by saving their brains!"],
            ["The game ends when...", "   You have no life", "   You have collected all 10 brains", "   A fluff eats one of the brains"],
            ["There are many items to aid", "you on your path", "use them wisely", "otherwise..."],
            ["Good luck!"],
            ["Nothing will hapen!"],
            ["Collect the upcoming relic", "use it to aquire the brains", "the mechanic is the same", "as the one from the weapons"],
            ["story", "num. 7"],
        ]
        for i in text:
            self.texts.append(self.asset_handler.FONT.render3(i))

    # def progress(self):
    #     if self.stage + 1 >= len(self.texts):
    #         return

    #     self.stage += 1

    #     x, y = 0, 0

    #     y = SCREEN_INIT_HEIGHT - self.texts[self.stage].get_height()
    #     x = 50
    #     self.pos = (x, y)
    #     self.skip_rect.x = self.texts[self.stage].get_width() + y
    #     self.skip_rect.y = y
    #     self.visible = True

    def set_stage(self, stage_new:int):
        self.stage = stage_new

        x, y = 0, 0

        y = SCREEN_INIT_HEIGHT - self.texts[self.stage].get_height() - 50
        x = 50
        self.pos = (x, y)
        self.skip_rect.x = self.texts[self.stage].get_width() + x + 10
        self.skip_rect.y = y
        self.visible = True

    def draw(self, surf:pygame.Surface):
        if self.visible:
            surf.blit(self.texts[self.stage], self.pos)
            surf.blit(self.asset_handler.SKIP_TEXT, self.skip_rect.topleft)

    def on_click(self, pos:tuple[int, int]) -> bool:
        if self.visible:
            if self.skip_rect.collidepoint(pos):
                # self.progress()
                self.visible = False
                return True
        
        return False