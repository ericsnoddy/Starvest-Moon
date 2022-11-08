# pip install
import pygame as pg

# local
from settings import *

class Level:
    def __init__(self, game):
        self.game = game
        self.win = self.game.win

        # sprite groups
        self.all_sprites = pg.sprite.Group()


    def update(self):
        self.all_sprites.update()
    

    def draw(self):
        self.all_sprites.draw(self.win)


    def run(self):
        pass
