# pip install
import pygame as pg

# local
from settings import *
from player import *
from overlay import *

class Level:
    def __init__(self, game):
        self.game = game
        self.win = self.game.win

        # sprite groups and player setup
        self.all_sprites = pg.sprite.Group()
        self.player = Player(self.game, self.all_sprites)
        self.overlay = Overlay(self.win, self.player)


    def update(self):
        self.all_sprites.update()
        self.player.update()
    

    def draw(self):
        self.all_sprites.draw(self.win)


    def run(self):
        pass
