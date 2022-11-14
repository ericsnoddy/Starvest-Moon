# std lib
from collections import deque

# req
import pygame as pg
from pygame.locals import *

# local
from settings import *
from support import import_folder
from timer import Timer


class Player(pg.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites, tree_sprites, interaction_sprites):
        super().__init__(group)  # auto-adds class instance to sprite group   
        self.animations = {}
        self._import_assets()
        self.status = 'down_idle'
        self.sleep = False
        self.frame_index = 0  # animation frame
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.z = LAYERS['main']  # layer level

        # movement
        self.direction = pg.math.Vector2()
        self.pos = pg.math.Vector2(self.rect.center)
        self.speed = PLAYER_SPEED

        # collision
        self.hitbox = self.rect.copy().inflate(PLAYER_HITBOX_SCALE)
        self.collision_sprites = collision_sprites

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

        # inventory
        self.item_inventory = {
            'wood': 0,
            'apple': 0,
            'corn': 0,
            'tomato': 0
        }

        # interaction
        self.tree_sprites = tree_sprites
        self.interaction_sprites = interaction_sprites


    def update(self, dt):
        self.input()
        self.move(dt)
        self.get_status()
        self.get_target_pos()
        [timer.update() for timer in self.timers.values() if timer.active]
        self.animate(dt)        
        

    def use_tool(self):

        # soil
        if self.selected_tool == 'hoe':
            pass

        # trees
        elif self.selected_tool == 'axe':
            for tree in self.tree_sprites.sprites():
                if tree.rect.collidepoint(self.target_pos):
                    tree.damage()

        # watering
        elif self.selected_tool == 'water':
            pass


    def get_target_pos(self):
        offset_vector = pg.math.Vector2(PLAYER_TOOL_OFFSET[self.status.split('_')[0]])
        self.target_pos = self.rect.center + offset_vector


    def use_seed(self):
        pass


    def trade(self):
        pass


    def input(self):
        keys = pg.key.get_pressed()

        # do not accept key input while using tool
        if not self.timers['tool use'].active and not self.sleep:
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

            # misc interaction
            # new day (bed)
            if keys[K_RETURN]:
                # this is the old way to do it
                # interaction_point = [zone for zone in self.interaction_sprites.sprites() if zone.rect.collidepoint(self.rect)]
                interaction_point = pg.sprite.spritecollide(self, self.interaction_sprites, False)
                if interaction_point:
                    if interaction_point[0].name == 'Trader':
                        self.trade()
                    else:  # name = 'Bed'
                        self.status = 'left_idle'
                        self.sleep = True  # flag that triggers new day

    
    def collision_check(self, direction):
        for sprite in self.collision_sprites:
            if hasattr(sprite, 'hitbox') and sprite.hitbox.colliderect(self.hitbox):
                # keep player out of obstacle hitboxes by adjusting player pos after collision
                if direction == 'horizontal':
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                    self.pos.x = self.hitbox.centerx

                elif direction == 'vertical':
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom
                    self.rect.centery = self.hitbox.centery
                    self.pos.y = self.hitbox.centery


    def move(self, dt):
        # normalize the diagonal
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # calc framerate-independent speed
        speed_dt = self.speed * dt

        # horizontal
        self.pos.x += self.direction.x * speed_dt
        self.hitbox.centerx = round(self.pos.x)  # round to avoid truncating
        self.rect.centerx = self.hitbox.centerx
        self.collision_check('horizontal')

        # vertical
        self.pos.y += self.direction.y * speed_dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision_check('vertical')


    def get_status(self):

        # idle
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

        # tool use
        if self.timers['tool use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool


    def animate(self, dt):
        self.frame_index += PLAYER_ANIM_RATE * dt  # fractionally increase frame_index (FPS independent) as timer
        self.frame_index %= len(self.animations[self.status])

        # if self.frame_index >= len(self.animations[self.status]):
        #     self.frame_index = 0
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

        
