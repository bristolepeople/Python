import random
#using pygame python GUI 
import pygame
import time
pygame.init()

# Setting the width and height of the screen [width, height]
size = (800, 800)
screen = pygame.display.set_mode(size)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (128,128,128)
BLUE = (9, 128, 255)
class Cell(object):
    def __init__(self, screen, x, y):
        self.__screen = screen
        self._xLoc = x
        self._yLoc = y
        w, h = pygame.display.get_surface().get_size()
        self._width = 50
        self._height = self._width
        self._visited = False
        self._north = True
        self._west = True
        self._east = True
        self._south = True
        self._colour = GREY 

    def draw(self):
        """
            draws the cell on the screen.
        """
        pygame.draw.rect(screen, self._colour, (self._xLoc, self._yLoc, self._width, self._height), 0)

    def drawWalls(self):
         pygame.draw.rect(screen, BLACK, (self._xLoc, self._yLoc, self._width, self._height), 5)



def findUnvisited(grid):
    """
        Build a list of indecies for unvisited cells.
    """
    unvisited = []
    for x in range(len(grid)):
        for y in range(len(grid[1])):
            if not grid[x][y]._visited:
                unvisited.append((x,y))
    return unvisited


def startHunt(grid):
    # Find random unvisited cell.
    unvisited = findUnvisited(grid)
    first = random.choice(unvisited)
    return hunt(grid,first,unvisited)

def hunt(grid,cell,unvisited):
    
    grid[cell[0]][cell[1]]._visited = True
    grid[cell[0]][cell[1]]._colour = WHITE
    grid[cell[0]][cell[1]].draw()
    pygame.display.flip()
    time.sleep(0.5)

    pressed = False
    #while not pressed:
    #    ev = pygame.event.get()
    #    for event in ev:
    #        if event.type == pygame.MOUSEBUTTONUP:
    #            pressed = True
    
    unvisited.remove(cell)

    neighbours = [(cell[0]+1,cell[1]),(cell[0]-1,cell[1]),(cell[0],cell[1]+1),(cell[0],cell[1]-1)]

    unvisitedNeighbours = list(set(neighbours) & set(unvisited))
    if unvisitedNeighbours:
        next = random.choice(unvisitedNeighbours)
        hunt(grid,next,unvisited)    
    return grid

screen.fill(BLUE)

grid = []

size = 10

for x in range(size):

    row = []

    for i in range(size):
        row.append(Cell(screen, 100+i*50, 100 + x * 50))
    for c in row:
        c.draw()
        c.drawWalls()

    grid.append(row)


pygame.display.flip()

while findUnvisited(grid):
    grid = startHunt(grid)

pressed = False
while not pressed:
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.MOUSEBUTTONUP:
            pressed = True
