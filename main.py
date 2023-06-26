from sys import exit as sys_exit

import pygame

from data import Data
from start_screen import StartScreen
from in_game3 import InGame

pygame.init()

DATA = Data()

start_screen = StartScreen(DATA)
# in_game = InGame()

why_return = -1

while True:
    x = start_screen.start()
    start_screen.save()
    start_screen.reset()

    if x:
        break
    
    in_game = InGame(DATA, "maps/1")
    why_return = in_game.start()

    print(why_return)

    if why_return == 0:
        # X pressed
        break
    else:
        start_screen.set_text(why_return)
    # elif why_return == 1:
    #     # home button
    #     pass
    # elif why_return == 2:
    #     # no life
    #     pass
    # elif why_return == 3:
    #     # brain eaten by fluff
    #     pass

pygame.quit()
sys_exit()