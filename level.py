# pip install
import pygame as pg

# local
from settings import *
from support import *
from player import *
from overlay import *
from sprites import *
from pytmx.util_pygame import load_pygame


class Level:
    def __init__(self, game):
        self.game = game
        self.win = self.game.win

        # sprite groups and player setup
        self.all_sprites = CameraGroup()
        self.setup()        
        


    def setup(self):
        # load the tmx tilemap
        tmx_data = load_pygame('data/map.tmx')

        # house
        for layer in ['HouseFloor', 'HouseFurnitureBottom']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                GenericSprite((x * TS, y * TS), surf, [self.all_sprites], LAYERS['house bottom'])

        for layer in ['HouseWalls', 'HouseFurnitureTop']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                GenericSprite((x * TS, y * TS), surf, [self.all_sprites])

        # fence
        for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
            GenericSprite((x * TS, y * TS), surf, [self.all_sprites])

        # water
        water_frames = import_folder('graphics/water')
        for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
            Water((x * TS, y * TS), water_frames, [self.all_sprites])

        # trees

        # wildflowers

        # player
        self.player = Player(self.all_sprites)

        # ground
        GenericSprite(
            pos = (0, 0),
            surf = pg.image.load('graphics/world/ground.png').convert_alpha(),
            groups = [self.all_sprites],
            z = LAYERS['ground']
        )        

        # gui
        self.overlay = Overlay(self.player)


    def update(self):
        self.all_sprites.update(self.game.dt)
        self.player.update(self.game.dt)
    

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
