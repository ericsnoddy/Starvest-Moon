# std lib
from random import randint

# reqs
import pygame as pg
from pytmx.util_pygame import load_pygame

# local
from settings import *
from support import import_folder
from player import *
from overlay import *
from sprites import *
from transition import *
from soil import SoilLayer
from sky import Rain


class Level:
    def __init__(self):
        self.win = pg.display.get_surface()
        self.all_sprites = CameraGroup()
        self.collision_sprites = pg.sprite.Group()
        self.tree_sprites = pg.sprite.Group()
        self.interaction_sprites = pg.sprite.Group()  # 'Bed' and 'Trader'
        self.soil_layer = SoilLayer(self.all_sprites, self.collision_sprites)  # reqd by sprite_setup()
        self.sprite_setup()
        self.overlay = Overlay(self.player)  # gui
        self.transition = Transition(self.win, self.player, self.new_day)  # new day
        self.rain = Rain(self.all_sprites)
        self.raining = randint(0, 100) < RAIN_CHANCE
        self.soil_layer.raining = self.raining
        

    def sprite_setup(self):
        # load tmx tilemap
        tmx_data = load_pygame('data/map.tmx')

        # layers - no need to order

        # ground
        BasicSprite((0, 0), pg.image.load('graphics/world/ground.png').convert_alpha(), [self.all_sprites], LAYERS['ground'])

        # house
        for layer in ['HouseFloor', 'HouseFurnitureBottom']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                BasicSprite((x * TS, y * TS), surf, [self.all_sprites], LAYERS['house bottom'])

        for layer in ['HouseWalls', 'HouseFurnitureTop']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                BasicSprite((x * TS, y * TS), surf, [self.all_sprites])

        # fence
        for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
            BasicSprite((x * TS, y * TS), surf, [self.all_sprites, self.collision_sprites])

        # water
        water_frames = import_folder('graphics/water')
        for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
            AnimatedSprite((x * TS, y * TS), water_frames, [self.all_sprites])

        # trees
        for obj in tmx_data.get_layer_by_name('Trees'):
            Tree(
                pos = (obj.x, obj.y), 
                surf = obj.image, 
                groups = [self.all_sprites, self.collision_sprites, self.tree_sprites], 
                name = obj.name,
                add_func = self.inventory_add)

        # wildflowers
        for obj in tmx_data.get_layer_by_name('Decoration'):
            WildFlower((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])

        # invisible collision tiles
        for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
            BasicSprite((x * TS, y * TS), pg.Surface((TS, TS)), [self.collision_sprites])

        # player - grouped into first (all_sprites) but needs collision_/tree_sprites for ref
        for obj in tmx_data.get_layer_by_name('Player'):
            if obj.name == 'Start':
                self.player = Player(
                    pos = (obj.x, obj.y), 
                    group = self.all_sprites, 
                    collision_sprites = self.collision_sprites, 
                    tree_sprites = self.tree_sprites, 
                    interaction_sprites = self.interaction_sprites,
                    soil_layer = self.soil_layer)

            if obj.name == 'Bed':
                InteractionSprite((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

        
    def new_day(self):

        # grow plants
        self.soil_layer.update_plants()

        # regrow apples
        for tree in self.tree_sprites.sprites():
            for apple in tree.apple_sprites.sprites():
                apple.kill()
            if not tree.dead:
                tree.create_fruit()
                tree.heal()

        # absorb water
        self.soil_layer.absorb_water()

        # chance of rain
        self.raining = self.soil_layer.raining = randint(1, 100) < RAIN_CHANCE
        if self.soil_layer.raining:
            self.soil_layer.water_all()


    def plant_collision(self):
        if self.soil_layer.plant_sprites:
            for plant in self.soil_layer.plant_sprites.sprites():
                if plant.harvestable and plant.rect.colliderect(self.player.hitbox):
                    self.inventory_add(plant.plant)
                    self.soil_layer.grid[plant.rect.centery // TS][plant.rect.centerx // TS].remove('P')
                    plant.kill()
                    Particle((plant.rect.x, plant.rect.y), plant.image, self.all_sprites)
                    

    def inventory_add(self, item, amount=1):
        # this is a method we'll pass to harvestable objects
        self.player.item_inventory[item] += amount


    def update(self, dt):
        self.all_sprites.update(dt)
        if self.raining:
            self.rain.update()
        self.plant_collision()


    def draw(self):
        self.win.fill('black')
        self.all_sprites.draw(self.win, self.player)
        self.overlay.draw(self.win)


    def run(self, dt):
        self.update(dt)
        self.draw()

        if self.player.sleep:
            self.transition.sleep(dt)  # calls self.new_day()



class CameraGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pg.math.Vector2()


    def draw(self, win, player):
        # keep the player at center of screen by offsetting everything relative to player
        self.offset.x = player.rect.centerx - WIDTH / 2
        self.offset.y = player.rect.centery - HEIGHT / 2

        # draw the sprites in order of layer first, y-value 2nd
        # no need to sort LAYERS.values() bc Python retains Dict insertion order
        for layer in LAYERS.values():
            # sort by ascending y-value, drawing top to bottom for pseudo-3D overlap
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    win.blit(sprite.image, offset_rect)
