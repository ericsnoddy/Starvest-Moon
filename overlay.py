# pip install
import pygame as pg

# local
from settings import *
from support import *

class Overlay:
    def __init__(self, player):
        self.player = player

        # imports
        overlay_path = 'graphics/overlay/'
        self.tool_surfs = {tool: pg.image.load(f'{overlay_path}{tool}.png').convert_alpha() for tool in self.player.tools}
        self.seed_surfs = {seed: pg.image.load(f'{overlay_path}{seed}.png').convert_alpha() for seed in self.player.seeds}

    def draw(self, win):
        # tools
        tool_surf = self.tool_surfs[self.player.selected_tool]
        tool_rect = tool_surf.get_rect(midbottom = OVERLAY_POSITIONS['tool'])
        win.blit(tool_surf, tool_rect)
        # seeds
        seed_surf = self.seed_surfs[self.player.selected_seed]
        seed_rect = seed_surf.get_rect(midbottom = OVERLAY_POSITIONS['seed'])
        win.blit(seed_surf, seed_rect)