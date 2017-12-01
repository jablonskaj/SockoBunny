import pygame
from pygame.math import Vector2
import Map

def indexToPos(board, index, vec = Vector2(0,0)):
    #returns start-position of indexed tile
    return Vector2(board.y_upBorder() + index[1] * tile_size,board.x_leftBorder() + index[0] * tile_size) + vec

def PosToIndex(board, position):
    #Returns index of tile which lays on the position
    y = int((position[0] - board.x_leftBorder()) / tile_size)
    x = int((position[1] - board.y_upBorder()) / tile_size)
    return [int(x), int(y)]

tile_size = 50
step = 2  # pixel-movement number
rad =  20 # radius od object
box = pygame.image.load('box.png')
box = pygame.transform.scale(box, (tile_size-5, tile_size-5))
box2 = pygame.image.load('carrot.png')
box2 = pygame.transform.scale(box2, (tile_size, tile_size))

bunny = pygame.image.load('bunny.png')
bunny = pygame.transform.scale(bunny, (tile_size, tile_size))
bunny2 = pygame.image.load('bunny2.png')
bunny2 = pygame.transform.scale(bunny2, (tile_size, tile_size))

class Object(object):    # objekt na planszy zdolny do ruchu

    def __init__(self, game, index):
        self.game = game
        self.index = Vector2(int(index[0]),int(index[1])) #
        self.pos = indexToPos(self.game.board,index) # position on th screen up-left corner
        self.angle = 0
        self.isMoving = {'D': 0, 'U': 0, 'L': 0, 'R': 0}
        # D #U #L #R

    def goDown(self):
        self.pos += (0, step)
        self.angle = 180
        self.index = PosToIndex(self.game.board, self.pos)

    def goUp(self):
        self.pos += (0, -step)
        self.angle = 0
        self.index = PosToIndex(self.game.board, self.pos)

    def goRight(self):
        self.pos += (step, 0)
        self.angle = 90
        self.index = PosToIndex(self.game.board, self.pos)

    def goLeft(self):
        self.pos -= (step, 0)
        self.angle = 270
        self.index = PosToIndex(self.game.board, self.pos)

    def tick(self):
        pressed = pygame.key.get_pressed()
        if (pressed[pygame.K_DOWN] and sum(self.isMoving.values()) == 0) or self.isMoving["D"]:  # if key 'down' is pressed OR was pressed, but spirit didnt get proper position, for example half of the square
            self.isMoving["D"] = True  # condition in braces - pressed button move the spirit just in case spirit is not moving in other direction
            self.goDown()
            if self.pos[1] == indexToPos(self.game.board, self.index)[1]:  # when spirit's position is correct (centered on the tile) stop moving
                self.isMoving["D"] = False
        elif (pressed[pygame.K_UP] and sum(self.isMoving.values()) == 0) or self.isMoving["U"]:
            self.isMoving["U"] = True
            self.goUp()
            if self.pos[1] == indexToPos(self.game.board, self.index)[1]:
                self.isMoving["U"] = False
        elif (pressed[pygame.K_LEFT] and sum(self.isMoving.values()) == 0) or self.isMoving["L"]:
            self.isMoving["L"] = True
            self.goLeft()
            if self.pos[0] == indexToPos(self.game.board, self.index)[0]:
                self.isMoving["L"] = False
        elif (pressed[pygame.K_RIGHT] and sum(self.isMoving.values()) == 0) or self.isMoving["R"]:
            self.isMoving["R"] = True
            self.goRight()
            if self.pos[0] == indexToPos(self.game.board, self.index)[0]:
                self.isMoving["R"] = False
    def draw(self):
        pass

class Player(Object) :   # gracz

    def __init__(self, game,index):
        super().__init__(game,index)


    def goRight(self):
        afterMove = PosToIndex(self.game.board, self.pos) + Vector2(0,1)
        if self.game.blockedTable[int(afterMove[0]),int(afterMove[1])] == 0 : # jeśli z prawej wolne
            super().goRight()
        elif self.game.blockedTable[int(afterMove[0]),int(afterMove[1])] == 1: # jeśłi z prawej skrzynka
            afterMove2 = afterMove + Vector2(0,1)
            if self.game.blockedTable[int(afterMove2[0]), int(afterMove2[1])] == 0: # jeśli za skrzynką wolne
                super().goRight()

    def goLeft(self):
        afterMove = PosToIndex(self.game.board, self.pos + Vector2(-1,0))
        if self.game.blockedTable[int(afterMove[0]),int(afterMove[1])] == 0:
            super().goLeft()
        elif self.game.blockedTable[int(afterMove[0]),int(afterMove[1])] == 1:
            afterMove2 = afterMove - Vector2(0,1)
            if self.game.blockedTable[int(afterMove2[0]), int(afterMove2[1])] == 0: # jeśli za skrzynką wolne
                super().goLeft()

    def goUp(self):
        afterMove = PosToIndex(self.game.board, self.pos + Vector2(0,-1))
        if self.game.blockedTable[int(afterMove[0]), int(afterMove[1])] == 0:
            super().goUp()
        elif self.game.blockedTable[int(afterMove[0]),int(afterMove[1])] == 1:
            afterMove2 = afterMove - Vector2(1,0)
            if self.game.blockedTable[int(afterMove2[0]), int(afterMove2[1])] == 0: # jeśli za skrzynką wolne
                super().goUp()
    def goDown(self):
        afterMove = PosToIndex(self.game.board, self.pos - Vector2(0,0)) + Vector2(1,0)
        if self.game.blockedTable[int(afterMove[0]), int(afterMove[1])] == 0:
            super().goDown()
        elif self.game.blockedTable[int(afterMove[0]),int(afterMove[1])] == 1: # jeśłi z prawej skrzynka
            afterMove2 = afterMove + Vector2(1,0)
            if self.game.blockedTable[int(afterMove2[0]), int(afterMove2[1])] == 0: # jeśli za skrzynką wolne
                super().goDown()

    def draw(self):
        super().draw()
        #self.game.screen.blit(ghost, self.pos)
        if self.angle == 270:
            self.game.screen.blit(bunny2, self.pos)
        else:
            self.game.screen.blit(bunny, self.pos)

# --------------------------------- BOX --------------------------------------

class Box(Object):
    def __init__(self, game, index):
        super().__init__(game, index)

    def right_downPos(self):
        return self.pos + Vector2(tile_size-1,tile_size-1)
    def right_downIndex(self):
        return PosToIndex(self.game.board, self.right_downPos())



    def goRight(self):
        if self.game.player.index[1] == self.index[1]-1 and self.game.player.index[0] == self.index[0]: # jeśłi ludek dotyka pudełka
           # if self.game.player.isMoving["R"] or self.isMoving['R']:
           if not self.game.player.isMoving["L"] and not self.game.player.isMoving["U"] and not \
           self.game.player.isMoving["D"]:
                afterMove = self.index + Vector2(0, 1) # index po przesunięciu w prawo
                if self.game.blockedTable[int(afterMove[0]), int(afterMove[1])] == 0: # jeśłi z prawej wolne
                    self.game.blockedTable[int(self.index[0]),int(self.index[1])] = 0 # skasuj skrzynkę z mapy
                    super().goRight()
                    self.game.blockedTable[int(self.index[0]), int(self.index[1])] = 1 #dodaj skrzynkę do mapy
    def goLeft(self):
       if self.game.player.pos[0] == self.pos[0] + tile_size and self.game.player.index[0] == self.index[0]: # jeśli ludek dotyka pudełka
            #if self.game.player.isMoving["L"] or self.isMoving['L']:
            if not self.game.player.isMoving["D"] and not self.game.player.isMoving["U"] and not \
            self.game.player.isMoving["R"]:                                             # prevention against moving box of half - distance while quick changing pressed buttons
                afterMove = self.right_downIndex() - Vector2(0,1)
                if self.game.blockedTable[int(afterMove[0]), int(afterMove[1])] == 0:
                    self.game.blockedTable[int(self.right_downIndex()[0]), int(self.right_downIndex()[1])] = 0  # skasuj skrzynkę z mapy
                    super().goLeft()
                    self.game.blockedTable[int(self.right_downIndex()[0]), int(self.right_downIndex()[1])] = 1  # dodaj skrzynkę do mapy
    def goUp(self):
        if self.game.player.pos[1] == self.pos[1] + tile_size and self.game.player.index[1] == self.index[1]: # czy ludek jest obok skrzynki
            # if self.game.player.isMoving["U"] or self.isMoving['U']:
            if not self.game.player.isMoving["L"] and not self.game.player.isMoving["D"] and not self.game.player.isMoving["R"]:
                afterMove = self.right_downIndex() - Vector2(1,0)
                if self.game.blockedTable[int(afterMove[0]), int(afterMove[1])] == 0:
                    self.game.blockedTable[int(self.right_downIndex()[0]), int(self.right_downIndex()[1])] = 0  # skasuj skrzynkę z mapy
                    super().goUp()
                    self.game.blockedTable[int(self.right_downIndex()[0]), int(self.right_downIndex()[1])] = 1
    def goDown(self):
        if self.game.player.index[0] == self.index[0] - 1 and self.game.player.index[1] == self.index[1]:
            #if self.game.player.isMoving["D"] or self.isMoving['D']:
            if not self.game.player.isMoving["L"] and not self.game.player.isMoving["U"] and not self.game.player.isMoving["R"]:
                afterMove = self.index + Vector2(1, 0)  # index po przesunięciu w prawo
                if self.game.blockedTable[int(afterMove[0]), int(afterMove[1])] == 0:  # jeśłi z prawej wolne
                    self.game.blockedTable[int(self.index[0]), int(self.index[1])] = 0  # skasuj skrzynkę z mapy
                    super().goDown()
                    self.game.blockedTable[int(self.index[0]), int(self.index[1])] = 1  # dodaj skrzynkę do mapy

    def tick(self):
        super().tick()

    def draw(self):
        super().draw()
        if self.game.board.tile_list[int(self.index[0])][int(self.index[1])] != 'o':
            self.game.screen.blit(box, self.pos)
        else:
            self.game.screen.blit(box2, self.pos)
class Box_list(object):
    def __init__(self,game, lis): # lista współrzędnych
        self.game = game
        self.list = [Box(self.game,x) for x in lis]

    def draw(self):
        for x in self.list:
            x.draw()

    def tick(self):
        for x in self.list:
            x.tick()