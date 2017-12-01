import pygame, sys
from object import *
from Map import *
import numpy as np



class Game(object):

    def __init__(self, level , boxeslist, playerposition ,board = (), size = (1280, 720),tps = 30.):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.delta = 0.0
        self.tps = tps
        self.level = level

        self.screen = pygame.display.set_mode(size)
        fontObj = pygame.font.SysFont("comicsansms", 16)

        self.board = Tile_map(self,board)
        self.player =Player(self,playerposition)
        self.boxes = Box_list(self,boxeslist)
        self.blockedTable = blockedTable(self.board.tile_list,self.boxes.list)
        pygame.display.set_caption('Python game!  level ' + str(self.level+1) )
        # handling events
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    sys.exit()
                if self.isFinished() :
                    return
            if pygame.key.get_pressed()[pygame.K_r]:
                return


            # ticking
            self.delta += self.clock.tick() / 1000.0
            while self.delta > 1 / tps:
                self.tick()
                self.delta -= 1 / tps


            #drawing
            self.screen.fill((0,0,0))

            self.draw()
            self.screen.blit(fontObj.render('RESTART R', True, (250,250,250)), (2* size[0] / 5, size[1] * 0.93))
            pygame.display.flip()

    def tick(self):
        self.boxes.tick()
        self.player.tick()


    def draw(self):
        self.board.draw_map()
        self.boxes.draw()
        self.player.draw()

    def isFinished(self):
        for x in self.boxes.list :
            if self.board.tile_list[int(x.index[0])][int(x.index[1])] != 'o':
                return False
        return True


