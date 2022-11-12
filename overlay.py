# pip install
import pygame as pg

# local
from settings import *
from support import *

class Overlay:
    def __init__(self, disp_surf, player):

        # general setup
        self.win = disp_surf
        self.player = player

        # imports
        overlay_path = 'graphics/overlay/'
        self.tools_surf = {tool: pg.image.load(f'{overlay_path}{tool}.png').convert_alpha() for tool in self.player.tools}
        self.seeds_surf = {seed: pg.image.load(f'{overlay_path}{seed}.png').convert_alpha() for seed in self.player.seeds}
