# std lib
from random import randint, choice

# pip install
import pygame as pg

# local
from settings import *
from timer import Timer


class BasicSprite(pg.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)
        self.z = z



class AnimatedSprite(BasicSprite):
    def __init__(self, pos, frames, groups, z=LAYERS['water']):

        # animation setup
        self.frames = frames
        self.frame_index = 0

        super().__init__(pos, self.frames[self.frame_index], groups, z)


    def animate(self, dt):
        anim_speed_dt = ANIM_RATE * dt # frame independent anim speed
        self.frame_index += anim_speed_dt
        self.frame_index %= len(self.frames)
        self.image = self.frames[int(self.frame_index)]


    def update(self, dt):
        self.animate(dt)



class WildFlower(BasicSprite):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.copy().inflate(-20, -self.rect.height * 0.9)



class Tree(BasicSprite):
    def __init__(self, pos, surf, groups, name):
        super().__init__(pos, surf, groups)

        # tree attrs
        self.health = TREE_HEALTH
        self.dead = False
        self.stump_surf = pg.image.load(f"graphics/stumps/{'small' if name == 'Small' else 'large'}.png")
        self.invul_timer = Timer(200)

        # apples
        self.apple_surf = pg.image.load('graphics/fruit/apple.png').convert_alpha()
        self.apple_pos_list = APPLE_POS[name]
        self.apple_sprites = pg.sprite.Group()
        self.create_fruit()


    def update(self, dt):
        if not self.dead: 
            self.check_death()

    def damage(self):
        self.health -= 1
        if len(self.apple_sprites.sprites()) > 0:
            random_apple = choice(self.apple_sprites.sprites())
            random_apple.kill()


    def check_death(self):
        if self.health <= 0:
            self.image = self.stump_surf
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
            self.hitbox = self.rect.copy().inflate(-10,  -self.rect.height * 0.6)
            self.dead = True

    
    def create_fruit(self):
        for apple_pos in self.apple_pos_list:
            if randint(0, 10) < 2:
                BasicSprite(
                    pos=(apple_pos[0] + self.rect.left, apple_pos[1] + self.rect.top), # apple_pos is relative to the screen position
                    surf=self.apple_surf,
                    # self.groups() is a clever pg.sprite.Group method to get access to level.all_sprites
                    # it returns a list of all groups the Tree obj belongs to, in order of insertion
                    groups=[self.apple_sprites, self.groups()[0]], 
                    z=LAYERS['fruit'])