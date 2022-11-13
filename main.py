# std lib
import sys

# pip install
import pygame as pg

# local
from settings import *
from level import Level

class Game:
    def __init__(self):
        pg.init()
        self.win = pg.display.set_mode((RES))
        self.clock = pg.time.Clock()
        self.dt = 1 # init
        self.level = Level()


    def run(self):
        while True:
            self.level.run(self.dt)
            self.check_events()
            self.update()
            self.draw()


    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()


    def update(self):
        self.dt = self.clock.tick(FPS) / 1000
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')
        pg.display.flip()


    def draw(self):
        self.win.fill('black')


if __name__ == '__main__':
    game = Game()
    game.run()