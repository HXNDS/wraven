import sys
import pygame as pg
from pygame.locals import *

pg.init()

class Player:

    def __init__(self):
        super().__init__()
        self.rect = pg.Rect(150,100,16,16)
        self.player_img = 0
        self.JUMPING = True 
        self.moving_right = False
        self.moving_left = False
        self.vertical_momentum = 0
        self.air_timer = 0

        self.flip = False
        self.frame = 0
        self.action = 'idle'

    def eventHandler(self):
        pass


class MapLoader:

    def __init__(self):
        self.load_map("DreadedCourts")

    def load_map(self,path):
        f = open(path + '.txt','r')
        data = f.read()
        f.close()
        data = data.split('\n')
        game_map = []
        for row in data:
            game_map.append(list(row))
        print(game_map)
        #return game_map


class Game:

    def __init__(self):
        super().__init__()

        """Gen Config"""
        self.WINDOWSIZE = (800,600)
        self.screen = pg.display.set_mode(self.WINDOWSIZE, 0, 32)
        self.display = pg.Surface((self.WINDOWSIZE[0]/2, self.WINDOWSIZE[1]/2))
        pg.display.set_caption("WRAVEN")


        """Game Vars"""
        self.running = True
        self.clock = pg.time.Clock()
        self.FPS = 60
        self.true_scroll = [0,0]
        self.bg = (0,0,0)

        """Method Calls"""
        self.eventHandler()

    def fillScreen(self):
        self.display.fill(self.bg)

    def eventHandler(self):
        
        self.ML = MapLoader()
        while self.running:
            self.fillScreen()
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    print("\nGAME CLOSED\n")
                    sys.exit()
            
            """Screen Refresh"""
            self.screen.blit(pg.transform.scale(self.display, self.WINDOWSIZE), (0,0))
            pg.display.update()
            self.clock.tick(self.FPS)
        




if __name__ == "__main__":
    game = Game()
