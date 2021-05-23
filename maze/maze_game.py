import random
#using pygame python GUI 
import pygame
import time
pygame.init()

# Setting the width and height of the screen [width, height]
size = (1200, 700)
screen = pygame.display.set_mode(size)
cellSize = 20
wallThickness = 2

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
        self._width = cellSize
        self._height = cellSize
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
        pygame.draw.rect(screen, self._colour, (self._xLoc + (wallThickness/2), self._yLoc + (wallThickness/2), self._width -(wallThickness/2) , self._height - (wallThickness/2)), 0)

    def drawWalls(self):
        if self._north:
            pygame.draw.rect(screen, BLACK, (self._xLoc , self._yLoc, self._width , wallThickness), 0)
        else:
            pygame.draw.rect(screen, WHITE, (self._xLoc + wallThickness , self._yLoc, self._width -wallThickness , wallThickness), 0)
        if self._south:
            pygame.draw.rect(screen, BLACK, (self._xLoc  , self._yLoc + self._height  , self._width , wallThickness), 0)
        else:
            pygame.draw.rect(screen, WHITE, (self._xLoc + wallThickness, self._yLoc + self._height  , self._width - wallThickness, wallThickness), 0)
        if self._west:
            pygame.draw.rect(screen, BLACK, (self._xLoc, self._yLoc , wallThickness, self._height  ), 0)
        else:
            pygame.draw.rect(screen, WHITE, (self._xLoc, self._yLoc + wallThickness , wallThickness, self._height - wallThickness), 0)
        if self._east:
            pygame.draw.rect(screen, BLACK, (self._xLoc + self._width , self._yLoc , wallThickness, self._height ), 0)
        else:
            pygame.draw.rect(screen, WHITE, (self._xLoc + self._width , self._yLoc  + wallThickness , wallThickness, self._height  -wallThickness ), 0)

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

def findFirstUnvisitedWithVisitedNeighbour(grid):
    rightToLeft = bool(random.getrandbits(1))
    bottomToTop = bool(random.getrandbits(1))
    
    xRange = range(len(grid))
    if rightToLeft:
        xRange = reversed(xRange)
    yRange = range(len(grid[0]))
#    if bottomToTop:
#        yRange = reversed(yRange)
    for x in xRange:
        for y in yRange:
            if grid[x][y]._visited:
                unvisitedNeighbours = findUnvisitedNeighbours((x,y), grid)
                if unvisitedNeighbours:
                    return ((x,y))

def findUnvisitedNeighbours(cell,grid):
    neighbours = [(cell[0]+1,cell[1]),(cell[0]-1,cell[1]),(cell[0],cell[1]+1),(cell[0],cell[1]-1)]
    myUnvisitedNeighbours = list(set(neighbours) & set(findUnvisited(grid)))
    return myUnvisitedNeighbours

def startHunt(grid):
    # Find random unvisited cell.
    unvisited = findUnvisited(grid)
    first = random.choice(unvisited)
    return hunt(grid,first,unvisited)

def continueHunt(grid):
    # Find random unvisited cell.
    cell = findFirstUnvisitedWithVisitedNeighbour(grid)
    unvisited = findUnvisited(grid)
    return hunt(grid,cell,unvisited)

def hunt(grid,cell,unvisited):
    
    grid[cell[0]][cell[1]]._visited = True
    grid[cell[0]][cell[1]]._colour = WHITE
    grid[cell[0]][cell[1]].draw()    
    grid[cell[0]][cell[1]].drawWalls()
    
    pressed = False
    
    if cell in unvisited: unvisited.remove(cell)

    neighbours = [(cell[0]+1,cell[1]),(cell[0]-1,cell[1]),(cell[0],cell[1]+1),(cell[0],cell[1]-1)]

    unvisitedNeighbours = list(set(neighbours) & set(unvisited))
    if unvisitedNeighbours:
        next = random.choice(unvisitedNeighbours)
        if next[1] < cell[1]:
            grid[next[0]][next[1]]._east = False
            grid[cell[0]][cell[1]]._west = False
        if next[1] > cell[1]:
            grid[next[0]][next[1]]._west = False
            grid[cell[0]][cell[1]]._east = False
        if next[0] < cell[0]:
            grid[next[0]][next[1]]._south = False
            grid[cell[0]][cell[1]]._north = False
        if next[0] > cell[0]:
            grid[next[0]][next[1]]._north = False
            grid[cell[0]][cell[1]]._south = False            

        grid[cell[0]][cell[1]].drawWalls()
        grid[next[0]][next[1]].drawWalls()

        pygame.display.flip()
        #time.sleep(0.01)
        hunt(grid,next,unvisited)  

    return grid

screen.fill(BLUE)

grid = []



for y in range(30):

    row = []

    for x in range(50):
        row.append(Cell(screen, 10+x*cellSize, 10 + y * cellSize))
    for c in row:
        c.draw()
        c.drawWalls()

    grid.append(row)


pygame.display.flip()

grid = startHunt(grid)
while findUnvisited(grid):
    grid = continueHunt(grid)

pressed = False
while not pressed:
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.MOUSEBUTTONUP:
            pressed = True
