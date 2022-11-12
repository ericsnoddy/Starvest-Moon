# pip install
import pygame as pg

# local
from settings import *

class GenericSprite(pg.sprite.Sprite):
    def __init__(self, pos, surf, groups, z = LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z



class Water(GenericSprite):
    def __init__(self, pos, frames, groups):

        # animation setup
        self.frames = frames
        self.frame_index = 0

        super().__init__(pos, self.frames[self.frame_index], groups, LAYERS['water'])


    def animate(self, dt):
        anim_speed = WATER_ANIM_RATE * dt # frame independent anim speed
        self.frame_index += anim_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]


    def update(self, dt):
        self.animate(dt)


class WildFlower(GenericSprite):
    def __init__(self, pos, frames, groups):
        self.frames = frames
        self.frame_index = 0
        super().__init__(pos, self.frames[self.frame_index], groups, LAYERS['water'])