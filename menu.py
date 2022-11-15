# reqs
import pygame as pg

# local
from settings import *


class Menu:
    def __init__(self, player, toggle_menu_func):
        self.player = player
        self.toggle_menu = toggle_menu_func
        self.font = pg.font.Font('font/LycheeSoda.ttf', 30)

        # options
        self.width = MENU_WIDTH
        self.space = MENU_SPACE
        self.padding = MENU_PADDING

    def draw(self, win):
        win.blit(pg.Surface((1000, 1000)), (0,0))


    def input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            self.toggle_menu()
        
