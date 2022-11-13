# pip install
import pygame as pg

# local
from settings import *
from player import Player
from overlay import Overlay

class Level:
    def __init__(self):
        self.win = pg.display.get_surface()

        # sprite groups
        self.all_sprites = pg.sprite.Group()
        self.setup()        


    def setup(self):
        self.player = Player(START_POS, self.all_sprites)
        self.overlay = Overlay(self.player)


    def update(self, dt):
        self.all_sprites.update(dt)


    def draw(self):
        self.all_sprites.draw(self.win)
        self.overlay.draw(self.win)


    def run(self, dt):
        self.update(dt)
        self.draw()