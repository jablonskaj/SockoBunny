import pygame
import numpy as np

tile_size = 50
#ładowanie grafiki
wall = pygame.image.load('wall.png')
wall = pygame.transform.scale(wall, (tile_size, tile_size))
tree = pygame.image.load('tree.png')
tree = pygame.transform.scale(tree, (tile_size, tile_size))
grass = pygame.image.load('grass.png')
grass = pygame.transform.scale(grass, (tile_size, tile_size))
grass2 = pygame.image.load('grass2.png')
grass2 = pygame.transform.scale(grass2, (tile_size, tile_size))
tree2 = pygame.image.load('tree2.png')
tree2 = pygame.transform.scale(tree2, (tile_size, tile_size))
garage = pygame.image.load('boxop.png')
garage= pygame.transform.scale(garage, (tile_size, tile_size))

#płytki
class Tile(object):
    def __init__(self, size):
        self.size = size

    def draw_tile(self,screen,loc):
        pass
class Grass(Tile):
    def __init__(self,size):
        super().__init__(size)

    def draw_tile(self, screen, loc):
        screen.blit(grass, loc)
class Wall(Tile):
    def __init__(self,size):
        super().__init__(size)
        #self.image =  pygame.image.load('wall')
    def draw_tile(self, screen, loc):
        screen.blit(wall,loc)
class Garage(Tile):
    def __init__(self,size):
        super().__init__(size)
    def draw_tile(self, screen, loc):
        pygame.draw.rect(screen,(153, 204, 51), pygame.Rect(loc[0],loc[1],self.size,self.size))
        screen.blit(garage, loc)
class Outside(Tile):
    def __init__(self,size):
        super().__init__(size)
    def draw_tile(self, screen, loc):
        screen.blit(grass2, loc)
class Tree(Tile):
    def __init__(self,size):
        super().__init__(size)
    def draw_tile(self, screen, loc):
        screen.blit(grass2, loc)
        screen.blit(tree, loc)
class Tree2(Tile):
    def __init__(self,size):
        super().__init__(size)
    def draw_tile(self, screen, loc):
        screen.blit(grass2, loc)
        screen.blit(tree2, loc)

image_dict = {
    "grass" : Grass(tile_size),
    "wall"  : Wall(tile_size),
    "garage": Garage(tile_size),
    "out"   : Outside(tile_size),
    "tree"  : Tree(tile_size),
    "tree2" : Tree2(tile_size)
}

tile_maping = {
    ' ': image_dict["grass"],
    '#': image_dict["wall"],
    'o': image_dict["garage"],
    'x': image_dict["out"],
    '1': image_dict["tree"],
    '2': image_dict["tree2"]
}

class Tile_map(object):

    def __init__(self, game, tile_list):
        self.game = game
        self.tile_list = tile_list

    def x_leftBorder(self):
        center_x = self.game.screen.get_size()[0] / 2
        return center_x - len(self.tile_list[0])*tile_size/2 # początek mapy x
    def y_upBorder(self):
        center_y = self.game.screen.get_size()[1] / 2
        return center_y - len(self.tile_list)*tile_size/2    # początek mapy y

    def nr(self):
        return len(self.tile_list)  # wysokość planszy
    def nc(self):
        return len(self.tile_list[0]) #szerokość planszy

    def draw_map(self):
        # where to start drawing
        x_position = self.x_leftBorder()
        y_position = self.y_upBorder()

        for i in range(self.nr()):
            for j in range(self.nc()):
                tile_maping[self.tile_list[i][j]].draw_tile(self.game.screen,(x_position,y_position))
                x_position += tile_size
            y_position += tile_size
            x_position = self.x_leftBorder()

    def whatTypeofTileAreUOn(self, position):  # zakłądam że nie wyjde poza planszę
        x = int((position[0] - self.x_leftBorder) / tile_size)
        y = int((position[1]-self.y_upBorder) / tile_size)
        return self.tile_list[int(y)][int(x)]

def blockedTable(T,bl):
    L = np.zeros((len(T), len(T[0])), dtype=int)
    for i in range(len(T)):
        for  j in range(len(T[0])):
            if not (T[i][j] in ['o',' ']):
                L[i,j] = -1
    for x in bl:
        L[int(x.index[0]),int(x.index[1])] = 1
    return L