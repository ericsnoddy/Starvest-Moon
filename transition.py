# reqs
import pygame as pg

# local
from settings import *


class Transition:
    def __init__(self, win, player, reset_func):
        self.win = win
        self.player = player
        self.reset = reset_func
        self.image = pg.Surface((RES))
        self.color_val = 255
        self.trans_speed = TRANSITION_SPEED
        self.trans_complete = False


    def sleep(self, dt):

        # play sunset/sunrise transition effect
        self.color_val += self.trans_speed
        if self.color_val <= 0: 
            self.trans_speed *= -1 # reverse
            self.color_val = 0
        if self.color_val > 255:
            # transition is complete
            self.color_val = 255
            self.trans_speed = TRANSITION_SPEED
            self.player.sleep = False
            self.reset()
        
        # fill gradually changes color
        self.image.fill([self.color_val] * 3)
        # BLEND_RGB_MULT blends out the white values; the brighter the value, the less visible the px
        self.win.blit(self.image, (0, 0), special_flags = pg.BLEND_RGB_MULT)

            