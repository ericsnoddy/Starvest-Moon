# std lib
from random import randint, choice

# reqs
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



class InteractionSprite(BasicSprite):
    def __init__(self, pos, size, groups, name):
        super().__init__(pos, pg.Surface(size), groups)
        self.name = name



class WildFlower(BasicSprite):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.copy().inflate(-20, -self.rect.height * 0.9)



class Particle(BasicSprite):
    def __init__(self, pos, surf, groups, z=LAYERS['main'], duration=200):
        super().__init__(pos, surf, groups, z)
        self.start = pg.time.get_ticks()
        self.duration = duration

        # create a white mask (to "flash")
        mask_surf = pg.mask.from_surface(self.image)
        new_surf = mask_surf.to_surface()
        # now we have mask with transparent px black, all other px white
        new_surf.set_colorkey((0, 0, 0))  # set black as the transparency
        self.image = new_surf


    def update(self, dt):
        now = pg.time.get_ticks()
        if now - self.start > self.duration:
            self.kill()
        
        

class Tree(BasicSprite):
    def __init__(self, pos, surf, groups, name, add_func):
        super().__init__(pos, surf, groups)

        # tree attrs
        self.name = name
        self.start_health = self.health = int(f"{TREE_HEALTH_SM if name == 'Small' else TREE_HEALTH_LG}")
        self.dead = False        
        self.stump_surf = pg.image.load(f"graphics/stumps/{'small' if name == 'Small' else 'large'}.png")
        self.invul_timer = Timer(200)

        # apples
        self.apple_surf = pg.image.load('graphics/plants/apple.png').convert_alpha()
        self.apple_pos_list = APPLE_POS[name]
        self.apple_sprites = pg.sprite.Group()
        self.create_fruit()

        # harvest
        self.inventory_add = add_func

        # note: self.groups()[0] will be a reference to level.all_sprites
        # (sprite.groups() returns list of groups the sprite belongs to, in order of insertion)
        # this is a clever workaround for not having direct access to that group

    def update(self, dt):
        if not self.dead: 
            self.check_death()


    def heal(self):
        # trees can heal above their starting health depending on TREE_HEAL constant
        if self.health < self.start_health:
            self.health += TREE_HEAL

    def damage(self):
        self.health -= 1
        # remove an apple
        if len(self.apple_sprites.sprites()) > 0:
            random_apple = choice(self.apple_sprites.sprites())
            Particle(random_apple.rect.topleft, random_apple.image, self.groups()[0], LAYERS['fruit'])
            random_apple.kill()
            self.inventory_add('apple')


    def check_death(self):
        if self.health <= 0:
            Particle(self.rect.topleft, self.image, self.groups()[0], duration=250)
            self.image = self.stump_surf
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
            self.hitbox = self.rect.copy().inflate(-10,  -self.rect.height * 0.6)
            self.dead = True
            self.inventory_add('wood', int(f"{2 if self.name == 'Small' else 3}"))

    
    def create_fruit(self):
        for apple_pos in self.apple_pos_list:
            if randint(0, 10) < 2:
                BasicSprite(
                    pos=(apple_pos[0] + self.rect.left, apple_pos[1] + self.rect.top), # apple_pos is relative to the screen position
                    surf=self.apple_surf,                    
                    groups=[self.apple_sprites, self.groups()[0]], 
                    z=LAYERS['fruit'])
