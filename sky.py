# std lib
from random import randint, choice

# reqs
import pygame as pg

# local
from settings import *
from support import import_folder
from sprites import *


class Sky:
    def __init__(self):
        self.full_surf = pg.Surface((RES))
        self.start_color = [255, 255, 255]
        self.end_color = [38, 101, 189]


    def update(self, dt):
        for incr, value in enumerate(self.end_color):
            if self.start_color[incr] > value:
                self.start_color[incr] -= DAYLIGHT_SAVINGS_RATE * dt


    def draw(self, win):
        self.full_surf.fill(self.start_color)
        win.blit(self.full_surf, (0,0), special_flags = pg.BLEND_RGB_MULT)



class Drop(BasicSprite):
    def __init__(self, pos, surf, groups, z, moving):
        super().__init__(pos, surf, groups, z)
        self.lifetime = randint(500, 600)
        self.start_time = pg.time.get_ticks()
        self.moving = moving
        if self.moving:
            self.pos = pg.math.Vector2(self.rect.topleft)
            self.direction = pg.math.Vector2(-2, 4)
            self.speed = randint(250, 300)


    def update(self, dt):
        # update gets called by Group()
        if self.moving:
            speed_dt = self.direction * self.speed * dt
            self.pos += speed_dt
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        now = pg.time.get_ticks()
        if now - self.start_time >= self.lifetime:
            self.kill()



class Rain:
    def __init__(self, all_sprites):
        self.all_sprites = all_sprites
        self.rain_drops = import_folder('graphics/rain/drops/')
        self.rain_floor = import_folder('graphics/rain/floor')
        self.floor_w, self.floor_h = pg.image.load('graphics/world/ground.png').get_size()


    def create_floor(self):
        Drop(pos = (randint(0, self.floor_w), randint(0, self.floor_h)), 
             surf = choice(self.rain_floor), 
             groups = [self.all_sprites], 
             z = LAYERS['rain floor'], 
             moving = False)


    def create_drops(self):
        Drop(pos = (randint(0, self.floor_w), randint(0, self.floor_h)), 
             surf = choice(self.rain_drops), 
             groups = [self.all_sprites], 
             z = LAYERS['rain drops'], 
             moving = True)


    def update(self):
        self.create_floor()
        self.create_drops()