# std lib
from collections import deque

# pip install
import pygame as pg
from pygame.locals import *

# local
from settings import *
from support import import_folder
from timer import Timer


class Player(pg.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)  # auto-adds class instance to sprite group   
        self.animations = {}
        self._import_assets()
        self.status = 'down_idle'
        self.frame_index = 0  # animation frame
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.z = LAYERS['main']  # layer level

        # movement
        self.direction = pg.math.Vector2()
        self.pos = pg.math.Vector2(self.rect.center)
        self.speed = PLAYER_SPEED

        # timers
        self.timers = {
			'tool use': Timer(350, self.use_tool),
            'tool change': Timer(200),
            'seed use': Timer(350, self.use_seed),
            'seed change': Timer(200)
        }

        # tools
        self.tools = deque(['axe', 'hoe', 'water'])
        self.selected_tool = self.tools[0]

        # seeds
        self.seeds = deque(['corn', 'tomato'])
        self.selected_seed = self.seeds[0]


    def update(self, dt):
        self.input()
        self.move(dt)
        self.get_status()
        [timer.update() for timer in self.timers.values() if timer.active]
        self.animate(dt)        
        

    def use_tool(self):
        print(f'Using {self.selected_tool}')


    def use_seed(self):
        print(f'Using {self.selected_seed}')


    def input(self):
        keys = pg.key.get_pressed()

        # do not accept key input while using tool
        if not self.timers['tool use'].active:
            # x-direction
            if keys[K_a]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[K_d]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0

            # y-direction
            if keys[K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            # tool use
            if keys[K_SPACE]:
                self.timers['tool use'].activate()
                self.direction = pg.math.Vector2()
                self.frame_index = 0  # reset anim to frame 0

            # tool change
            if not self.timers['tool change'].active:
                if keys[K_LEFT]:
                    self.timers['tool change'].activate()
                    self.tools.rotate(-1)
                    self.selected_tool = self.tools[0]
                elif keys[K_RIGHT]:
                    self.timers['tool change'].activate()
                    self.tools.rotate(1)
                    self.selected_tool = self.tools[0]

            # seed use
            if keys[K_RCTRL]:
                self.timers['seed use'].activate()
                self.direction = pg.math.Vector2()
                self.frame_index = 0

            # seed change
            if not self.timers['seed change'].active:
                if keys[K_DOWN]:
                    self.timers['seed change'].activate()
                    self.seeds.rotate(-1)
                    self.selected_seed = self.seeds[0]
                elif keys[K_UP]:
                    self.timers['seed change'].activate()
                    self.seeds.rotate(1)
                    self.selected_seed = self.seeds[0]

            
    def move(self, dt):
        # normalize the diagonal
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # calc framerate-independent speed
        speed = self.speed * dt

        # horizontal
        self.pos.x += self.direction.x * speed
        self.rect.centerx = self.pos.x

        # vertical
        self.pos.y += self.direction.y * speed
        self.rect.centery = self.pos.y


    def get_status(self):

        # idle
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

        # tool use
        if self.timers['tool use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool


    def animate(self, dt):
        self.frame_index += PLAYER_ANIM_RATE * dt  # fractionally increase frame_index (FPS independent) as timer
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]  # index gradually increases until next int
    
    #
    # SUPPORT METHODS
    #
    def _import_assets(self):
        self.animations = {'up': [],'down': [],'left': [],'right': [],
						   'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
						   'right_hoe':[],'left_hoe':[],'up_hoe':[],'down_hoe':[],
						   'right_axe':[],'left_axe':[],'up_axe':[],'down_axe':[],
						   'right_water':[],'left_water':[],'up_water':[],'down_water':[]}

        # build a dict of lists of animation frames (img surfs), which are organized by player action
        for animation in self.animations.keys():
            full_path = 'graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)

        
