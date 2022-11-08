# std lib
import sys

# pip install
import pygame as pg

# local
from settings import *
from level import *
from player import *

class Game:
    def __init__(self):
        pg.init()
        self.win = pg.display.set_mode((RES))
        self.clock = pg.time.Clock()
        self.dt = 1 # init

        self.new_game()

    
    def new_game(self):
        # level must be run first
        self.level = Level(self)
        self.player = Player(self)
    

    def update(self):
        self.level.update()
        self.player.update()

        # display
        pg.display.flip()
        self.dt = self.clock.tick(FPS)  / 1000 # delta_time (sec)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')


    def draw(self):
        self.win.fill('black')
        self.level.draw()


    def check_events(self):
        # event loop
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()


    def run(self):
        # game loop
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
