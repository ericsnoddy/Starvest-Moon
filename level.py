# pip install
import pygame as pg
from pytmx.util_pygame import load_pygame

# local
from settings import *
from player import Player
from overlay import Overlay
from sprites import BasicSprite

class Level:
    def __init__(self):
        self.win = pg.display.get_surface()

        # sprite groups
        self.all_sprites = CameraGroup()
        self.setup()        


    def setup(self):
        # layers - no need to order
        BasicSprite((0, 0), pg.image.load('graphics/world/ground.png').convert_alpha(), [self.all_sprites], LAYERS['ground'])

        # player
        self.player = Player(START_POS, self.all_sprites)

        # gui
        self.overlay = Overlay(self.player)


    def update(self, dt):
        self.all_sprites.update(dt)


    def draw(self):
        self.all_sprites.draw(self.win, self.player)
        self.overlay.draw(self.win)


    def run(self, dt):
        self.update(dt)
        self.draw()



class CameraGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pg.math.Vector2()


    def draw(self, win, player):
        # keep the player at center of screen by offsetting everything relative to player
        self.offset.x = player.rect.centerx - WIDTH / 2
        self.offset.y = player.rect.centery - HEIGHT / 2

        # draw the sprites in order of layer
        # no need to sort LAYERS.values() bc Python retains Dict insertion order
        for layer in LAYERS.values():
            for sprite in self.sprites():
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    win.blit(sprite.image, offset_rect)
