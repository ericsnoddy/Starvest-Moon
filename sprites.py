# pip install
import pygame as pg

# local
from settings import *


class BasicSprite(pg.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z



class AnimatedSprite(BasicSprite):
    def __init__(self, pos, frames, groups, z=LAYERS['water']):

        # animation setup
        self.frames = frames
        self.frame_index = 0

        super().__init__(pos, self.frames[self.frame_index], groups, z)


    def animate(self, dt):
        anim_speed = ANIM_RATE * dt # frame independent anim speed
        self.frame_index += anim_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]


    def update(self, dt):
        self.animate(dt)



class Flora(BasicSprite):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)



class Tree(BasicSprite):
    def __init__(self, pos, surf, groups, name):
        super().__init__(pos, surf, groups)