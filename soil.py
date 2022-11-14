# reqs
import pygame as pg
from pytmx.util_pygame import load_pygame

# local
from settings import *


class SoilLayer:
    def __init__(self, all_sprites):

        # sprite groups
        self.all_sprites = all_sprites
        self.soil_sprites = pg.sprite.Group()

        # graphics
        self.soil_surf = pg.image.load('graphics/soil/o.png')

        # build self.grid, a list with data for every tile
        self.create_soil_grid()

    
    def create_soil_grid(self):
        # list for every tile holding data about the tile
        h_size, v_size = pg.image.load('graphics/world/ground.png').get_size()
        h_tiles, v_tiles = h_size // TS, v_size // TS

        # every tile will be a separate list
        # first create empty nested list ('rows'= v_tiles rows,  'row' elements = h_tiles cols):
        # [  [[], [], ...],    
        #    [[], [], ...],   ... ]
        self.grid = [[[] for col in range(h_tiles)] for row in range(v_tiles)]
        # flag farmable tiles with a simple 'F', using tmx data
        for x, y, _ in load_pygame('data/map.tmx').get_layer_by_name('Farmable').tiles():
            self.grid[x][y].append('F')
        

    

