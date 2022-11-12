# std lib
from collections import deque

# pip install
import pygame as pg
from pygame.locals import *
from support import *

# local
from settings import *
from timer import *

class Player(pg.sprite.Sprite):
    def __init__(self, game, group):
        super().__init__(group)
        self.game = game

        # init methods
        self.import_assets()    # inits self.animations

        # sprite attrs
        self.status = 'down_idle'
        self.frame_index = 0
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = START_POS)
        self.z = LAYERS['main'] # layer level, as in (x, y, z)

        # movement
        self.direction = pg.math.Vector2()
        self.pos = pg.math.Vector2(self.rect.center)
        self.speed = PLAYER_SPEED

        # timers
        self.timers = {
			'tool use': Timer(350, self.use_tool),
            'tool change': Timer(200),
            'seed': Timer(350, self.use_seed),
            'seed change': Timer(350)
        }

        # tools
        self.tools = deque(['axe', 'hoe', 'water'])
        self.selected_tool = self.tools[0]

        # seeds
        self.seeds = deque(['corn', 'tomato'])
        self.selected_seed = self.seeds[0]
        

    def update(self):
        self.input()
        self.movement()
        self.get_status()
        self.animate()
        for timer in self.timers.values():
            timer.update()


    def use_tool(self):
        pass


    def use_seed(self):
        pass


    def get_status(self):

        # idle
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

        # tool use
        if self.timers['tool use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool


    def movement(self):
        # frame independent speed
        speed = self.speed * self.game.dt

        # horizontal
        self.pos.x += self.direction.x * speed
        self.rect.centerx = self.pos.x

        # vertical
        self.pos.y += self.direction.y * speed
        self.rect.centery = self.pos.y


    def input(self):
        self.direction = pg.math.Vector2()
        keys = pg.key.get_pressed()

        # cannot move while using tool
        if not self.timers['tool use'].active:
            # directions
            if keys[K_w]:
                self.direction.y = -1
                self.status = 'up'

            elif keys[K_s]:
                self.direction.y = 1
                self.status = 'down'

            if keys[K_a]:
                self.direction.x = -1
                self.status = 'left'

            elif keys[K_d]:
                self.direction.x = 1
                self.status = 'right'

            if self.direction.magnitude() > 0:
                self.direction = self.direction.normalize()


            # change tool
            if not self.timers['tool change'].active:
                if keys[K_LEFT]:
                    self.timers['tool change'].activate()
                    self.tools.rotate(1)
                    self.selected_tool = self.tools[0]
                elif keys[K_RIGHT]:
                    self.timers['tool change'].activate()
                    self.tools.rotate(-1)
                    self.selected_tool = self.tools[0]

            # tool use
            if keys[K_SPACE]:
                self.timers['tool use'].activate()
                self.frame_index = 0 

            # change seed
            if not self.timers['seed change'].active:
                if keys[K_DOWN]:
                    self.timers['seed change'].activate()
                    self.seeds.rotate(1)
                    self.selected_seed = self.seeds[0]
                elif keys[K_UP]:
                    self.timers['seed change'].activate()
                    self.seeds.rotate(-1)
                    self.selected_seed = self.seeds[0]

            # use seed
            if keys[K_RCTRL]:
                self.timers['seed'].activate()
                self.frame_index = 0

            


    def animate(self):
        anim_speed = PLAYER_ANIM_RATE * self.game.dt # frame independent anim speed
        self.frame_index += anim_speed
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]


    def import_assets(self):
        self.animations = {'up': [],'down': [],'left': [],'right': [],
						   'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
						   'right_hoe':[],'left_hoe':[],'up_hoe':[],'down_hoe':[],
						   'right_axe':[],'left_axe':[],'up_axe':[],'down_axe':[],
						   'right_water':[],'left_water':[],'up_water':[],'down_water':[]}

        for animation in self.animations.keys():
            full_path = 'graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)


