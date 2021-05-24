import random
#using pygame python GUI 
import pygame
import time
pygame.init()

# Setting the width and height of the screen [width, height]
size = (1200, 700)
screen = pygame.display.set_mode(size)
cellSize = 6
wallThickness = 2

unvisited = []

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
    for x in range(len(grid)):
        for y in range(len(grid[1])):
            if not grid[x][y]._visited:
                unvisited.append((x,y))
    return unvisited

def findUnvisitedNeighbours(grid, cell):
    neighbours = [(cell[0]+1,cell[1]),(cell[0]-1,cell[1]),(cell[0],cell[1]+1),(cell[0],cell[1]-1)]
    unvistedNeighbours = []
    for cell in neighbours:
        if ((cell[0] >= 0) and (cell[0] < len(grid)) and (cell[1] >= 0) and (cell[1] < len(grid[0])) and (grid[cell[0]][cell[1]]._visited == False)):
            unvistedNeighbours.append(cell)
    return unvistedNeighbours

def findFirstUnvisitedWithVisitedNeighbour(grid):
    rightToLeft = bool(random.getrandbits(1))
    
    xRange = range(len(grid))
    if rightToLeft:
        xRange = reversed(xRange)
    yRange = range(len(grid[0]))
    for x in xRange:
        for y in yRange:
            if grid[x][y]._visited:
                unvisitedNeighbours = findUnvisitedNeighbours(grid,(x,y))
                if unvisitedNeighbours:
                    return ((x,y))

def startHunt(grid):
    # Find random unvisited cell.
    first = random.choice(unvisited)
    return hunt(grid,first)

def continueHunt(grid):
    # Find random unvisited cell.
    cell = findFirstUnvisitedWithVisitedNeighbour(grid)
   
    return hunt(grid,cell)

def hunt(grid,cell):
    
    grid[cell[0]][cell[1]]._visited = True
    grid[cell[0]][cell[1]]._colour = WHITE
    grid[cell[0]][cell[1]].draw()    
    grid[cell[0]][cell[1]].drawWalls()
    
    if cell in unvisited: unvisited.remove(cell)

    unvistedNeighbours = findUnvisitedNeighbours(grid, cell)

    if unvistedNeighbours:
        next = random.choice(unvistedNeighbours)
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

        grid = hunt(grid,next)  

    return grid

def createGrid(height, width):
    grid = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(Cell(screen, 10+x*cellSize, 10 + y * cellSize))
        for c in row:
            c.draw()
            c.drawWalls()
        grid.append(row)
    return grid

screen.fill(BLUE)
grid = createGrid(100,180)
pygame.display.flip()

unvisited = findUnvisited(grid)

grid = startHunt(grid)
pygame.display.flip()
while unvisited:
    grid = continueHunt(grid)
    pygame.display.flip()

pressed = False
while not pressed:
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.MOUSEBUTTONUP:
            pressed = True
