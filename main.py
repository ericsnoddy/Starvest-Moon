# std lib
import sys

# reqs
import pygame as pg

# local
from settings import *
from level import Level

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.win = pg.display.set_mode((RES))
        self.clock = pg.time.Clock()
        self.dt = 1 # init delta_time
        self.level = Level()


    def run(self):
        while True:
            self.level.run(self.dt)
            self.update()
            self.check_events()
            

    def update(self):
        self.dt = self.clock.tick(FPS) / 1000
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')  #  caption the framerate
        pg.display.flip()


    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run()