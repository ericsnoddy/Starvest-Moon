# std lib
from random import choice

# reqs
import pygame as pg
from pytmx.util_pygame import load_pygame

# local
from settings import *
from support import import_folder, import_folder_dict


class SoilTile(pg.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = LAYERS['soil']



class WaterTile(pg.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.image.set_alpha(125)
        self.rect = self.image.get_rect(topleft = pos)
        self.z = LAYERS['soil water']



class Plant(pg.sprite.Sprite):
    def __init__(self, plant, groups, soil, is_watered):
        super().__init__(groups)
        self.plant = plant
        self.soil = soil
        self.frames = import_folder(f'graphics/plants/{self.plant}/')
        self.age = 0
        self.max_age = len(self.frames) - 1
        self.grow_speed = GROW_SPEED[self.plant]
        
        # sprite setup
        self.image = self.frames[self.age]
        self.y_off = -16 if plant == 'corn' else -8
        self.rect = self.image.get_rect(midbottom = self.soil.rect.midbottom + pg.math.Vector2(0, self.y_off))
        self.z = LAYERS['ground plant']

        # Boolean method
        self.is_watered = is_watered
        self.harvestable = False

    
    def grow(self):
        if self.is_watered(self.rect.center):
            self.age += self.grow_speed

            # plant becomes obstacle
            if int(self.age) > 0:
                self.z = LAYERS['main']
                self.hitbox = self.rect.copy().inflate(-26, -self.rect.height * 0.4)

            # ripen
            if self.age >= self.max_age:
                self.age = self.max_age  # avoid index error
                self.harvestable = True
            self.image = self.frames[int(self.age)]
            self.rect = self.image.get_rect(midbottom = self.soil.rect.midbottom + pg.math.Vector2(0, self.y_off))


class SoilLayer:
    def __init__(self, all_sprites, collision_sprites):

        # sprite groups
        self.all_sprites = all_sprites
        self.collision_sprites = collision_sprites
        self.soil_sprites = pg.sprite.Group()
        self.water_sprites = pg.sprite.Group()
        self.plant_sprites = pg.sprite.Group()

        # graphics
        self.soil_surfs = import_folder_dict('graphics/soil')
        self.water_surfs = import_folder('graphics/soil_water')

        # build self.grid, a list with data for every tile
        self.create_soil_grid()
        self.create_hit_rects()

        # updated by Level()
        self.raining = False
    

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
            self.grid[y][x].append('F')
        

    def create_hit_rects(self):
        self.hit_rects = []
        for row_index, row in enumerate(self.grid):
            for col_index, cell in enumerate(row):
                # append a rect to every tile that is farmable
                if 'F' in cell:
                    self.hit_rects.append(pg.rect.Rect(col_index * TS, row_index * TS, TS, TS))


    def update_plants(self):
        [plant.grow() for plant in self.plant_sprites.sprites()]


    def get_hit(self, target_pos):
        for rect in self.hit_rects:
            if rect.collidepoint(target_pos):
                # convert to grid location
                x = rect.x // TS
                y = rect.y // TS
                if 'F' in self.grid[y][x]:
                    self.grid[y][x].append('X')  # flag as soil patch - y,x ?
                    self.create_soil_tiles()
                    if self.raining:
                        self.water_all()


    def water(self, target_pos):
        for sprite in self.soil_sprites.sprites():
            if sprite.rect.collidepoint(target_pos):
                x = sprite.rect.x // TS
                y = sprite.rect.y // TS
                if not 'W' in self.grid[y][x]:
                    self.grid[y][x].append('W')
                    WaterTile(sprite.rect.topleft, choice(self.water_surfs), [self.all_sprites, self.water_sprites])


    def water_all(self):
        for row_index, row in enumerate(self.grid):
            for col_index, cell in enumerate(row):
                if 'X' in cell and 'W' not in cell:
                    cell.append('W')
                    WaterTile((col_index * TS, row_index * TS), choice(self.water_surfs), [self.all_sprites, self.water_sprites])


    def plant_seed(self, target_pos, seed):
        for sprite in self.soil_sprites.sprites():
            if sprite.rect.collidepoint(target_pos):
                x, y = sprite.rect.x, sprite.rect.y
                self.grid[y // TS][x // TS].append('P')
                Plant(seed, [self.all_sprites, self.plant_sprites, self.collision_sprites], sprite, self.is_watered)


    def absorb_water(self):
        # destroy water sprites
        for sprite in self.water_sprites.sprites():
            sprite.kill()

        # clean up grid
        for row in self.grid:
            for cell in row:
                if 'W' in cell: cell.remove('W')


    def is_watered(self, pos):
        cell = self.grid[pos[1] // TS][pos[0] // TS]
        return True if 'W' in cell else False


    def create_soil_tiles(self):
        self.soil_sprites.empty()  # populate from scratch because tiles will change
        for row_index, row in enumerate(self.grid):
            for col_index, cell in enumerate(row):
                if 'X' in cell:

                    # check adjacent tile states for placing correct soil surf (Bool)
                    t = 'X' in self.grid[row_index - 1][col_index]
                    b = 'X' in self.grid[row_index + 1][col_index]
                    l = 'X' in row[col_index - 1]  # row = self.grid[row_index]
                    r = 'X' in row[col_index + 1]

                    # determine tile_type based on adjacent squares
                    tile_type = 'o' # default

                        # all
                    if all((t, b, l, r)): tile_type = 'x'

                        # horizontal
                    if l and not any((t, b, r)): tile_type = 'r'
                    if r and not any((t, b, l)): tile_type = 'l'
                    if l and r and not any((t, b)): tile_type = 'lr'

                        # vertical
                    if t and not any((b, l, r)): tile_type = 'b'
                    if b and not any((t, l, r)): tile_type = 't'
                    if t and b and not any((l, r)): tile_type = 'tb'

                        # quadrants
                    if t and l and not any((b, r)): tile_type = 'br'
                    if t and r and not any((b, l)): tile_type = 'bl'
                    if b and l and not any((t, r)): tile_type = 'tr'
                    if b and r and not any((t, l)): tile_type = 'tl'

                        # combined quadrants
                    if all((t, b, l)) and not r: tile_type = 'rm'
                    if all((t, b, r)) and not l: tile_type = 'lm'
                    if all((b, l, r)) and not t: tile_type = 'tm'
                    if all((t, l, r)) and not b: tile_type = 'bm'

                    SoilTile((col_index * TS, row_index * TS), 
                              self.soil_surfs[tile_type], [self.all_sprites, self.soil_sprites]) 

