# reqs
import pygame as pg

# local
from settings import *


class SoilLayer:
    def __init__(self, all_sprites):

        # sprite groups
        self.all_sprites = all_sprites
        self.soil_sprites = pg.sprite.Group()

        # graphics
        self.soil_surf = pg.image.load('graphics/soil/o.png')

        # build grid
        self.create_soil_grid()

    
    def create_soil_grid(self):
        # list for every tile holding data about the tile
        ground = pg.image.load('graphics/world/ground.png')
        h_tiles, v_tiles = ground.get_width() // TS, ground.get_height() // TS

