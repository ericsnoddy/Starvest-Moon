# pip install
import pygame as pg

# local
from settings import *
from player import *
from overlay import *
from sprites import *

class Level:
    def __init__(self, game):
        self.game = game
        self.win = self.game.win

        # sprite groups and player setup
        self.all_sprites = CameraGroup()
        self.setup()        
        


    def setup(self):
        GenericSprite(
            pos = (0, 0),
            surf = pg.image.load('graphics/world/ground.png').convert_alpha(),
            groups = [self.all_sprites],
            z = LAYERS['ground']
        )
        self.player = Player(self.game, self.all_sprites)
        self.overlay = Overlay(self.player)


    def update(self):
        self.all_sprites.update()
        self.player.update()
    

    def draw(self):
        # self.all_sprites.draw(self.win)
        self.all_sprites.draw(self.win, self.player)
        self.overlay.draw(self.win)


    def run(self):
        pass



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
