import math
import time
from random import randint
import os
import pygame

pygame.init()


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None
        self.H = 0
        self.G = 10000000000
        self.children = []
        self.isObstacle = False
        self.start = False
        self.goal = False

    def cost(self):
        if self.parent:
            return math.sqrt(((self.x - self.parent.x) ** 2) + ((self.y - self.parent.y) ** 2))
        else:
            return 0

    def isObstacle(self):
        return self.isObstacle

    def setObstacle(self):
        self.isObstacle = True

    def isStart(self):
        return self.start

    def setStart(self):
        self.start = True

    def isGoal(self):
        return self.goal

    def setGoal(self):
        self.goal = True


def ED(current, goal):
    if not current == goal:
        return math.sqrt(((goal.x - current.x) ** 2) + ((goal.y - current.y) ** 2))
    else:
        return 0


def araStar(start, goal, weight):
    openList = set()
    closedList = set()
    incumbent = []
    # s
    current = start
    current.G = 0

    # sets the start nodes heuristic
    current.H = ED(current, goal)

    # adds start to open list
    openList.add(current)

    # G
    pathCost = 100000000000000000

    # weight Delta
    weightDelta = weight / 2

    # while there are nodes in the open list
    while openList:
        NewSolution = improvedSolution(goal, openList, weight, pathCost)

        if NewSolution:
            pathCost = NewSolution[-1].G
            incumbent = NewSolution
            drawPath(incumbent, randomColor())
            time.sleep(.5)
        else:
            return incumbent

        weight = weight - weightDelta

        for child in current.children:
            if current.G + ED(current, child) < child.G:
                if child.isObstacle:
                    continue
                child.parent = current
                child.G = current.G + child.cost()
                child.H = ED(child, goal)

        for node in list(openList):
            if node.G + node.H >= pathCost:
                closedList.add(node)
                openList.remove(node)
    return incumbent


def improvedSolution(goal, openList, weight, pathCost):
    closedList = set()
    # while there are nodes in the open list
    while openList:

        current = min(openList, key=lambda o: o.G + (weight * o.H))

        openList.remove(current)
        closedList.add(current)

        # exits function if estimated travel is more than best path cost
        if pathCost <= current.G + (weight * current.H):
            # pathCost is proven to be w-admissible
            return None

        # for each child
        for node in current.children:
            # Duplicate detection and updating g(n`)
            if node.isObstacle:
                continue
            if node in closedList and node.G < current.G + node.cost():
                continue
            if node in openList and node.G < current.G + node.cost():
                continue
            if current.parent:
                current.G = current.parent.G + current.cost()

            drawRect(WHITE, node.x, node.y)
            pygame.display.update()

            # Prune nodes over the bound
            if node.G + node.H > pathCost:
                continue
            if node in openList:
                new_g = current.G + node.cost()
                if node.G > new_g:
                    node.G = new_g
                    node.parent = current
            else:
                node.parent = current
                node.G = current.G + node.cost()
                if not node == goal:
                    node.H = ED(node, goal)
                else:
                    path = []
                    while node.parent:
                        node = node.parent
                        path.append(node)
                    path.append(node)
                    return path[::-1]
                openList.add(node)
    return None


def drawRect(color, x, y):
    pygame.draw.rect(screen,
                     color,
                     [(MARGIN + GRID_SIZE) * x + MARGIN,
                      (MARGIN + GRID_SIZE) * y + MARGIN,
                      GRID_SIZE,
                      GRID_SIZE])


def north(grid, x, y, GRID_Y):
    if y > 0 and not grid[x][y - 1].isObstacle:
        return grid[x][y - 1]


def south(grid, x, y, GRID_Y):
    if y < GRID_Y - 1 and not grid[x][y + 1].isObstacle:
        return grid[x][y + 1]


def west(grid, x, y, GRID_X):
    if x > 0 and not grid[x - 1][y].isObstacle:
        return grid[x - 1][y]


def east(grid, x, y, GRID_X):
    if x < GRID_X - 1 and not grid[x + 1][y].isObstacle:
        return grid[x + 1][y]


def northEast(grid, x, y, GRID_X, GRID_Y):
    if x < GRID_X - 1 and y > 0 and not grid[x + 1][y - 1].isObstacle:
        return grid[x + 1][y - 1]


def southEast(grid, x, y, GRID_X, GRID_Y):
    if x < GRID_X - 1 and y < GRID_Y - 1 and not grid[x + 1][y + 1].isObstacle:
        return grid[x + 1][y + 1]


def northWest(grid, x, y, GRID_X, GRID_Y):
    if x > 0 and y > 0 and not grid[x - 1][y - 1].isObstacle:
        return grid[x - 1][y - 1]


def southWest(grid, x, y, GRID_X, GRID_Y):
    if x > 0 and y < GRID_Y - 1 and not grid[x - 1][y + 1].isObstacle:
        return grid[x - 1][y + 1]


def drawPath(path, color):
    for p in path:
        if not p == S and not p == G:
            drawRect(color, p.x, p.y)
            pygame.display.update()


def randomColor():
    return randint(0, 255), randint(0, 255), randint(0, 255)


GRID_SIZE = 10
GRID_X = 100
GRID_Y = 100
MARGIN = 2
os.environ['SDL_VIDEO_CENTERED'] = '1'
screen = pygame.display.set_mode(
    (GRID_X * GRID_SIZE + GRID_X * MARGIN + MARGIN, GRID_Y * GRID_SIZE + GRID_Y * MARGIN + MARGIN), pygame.RESIZABLE)
pygame.display.set_caption('A* Algorithm')
GRAY = (169, 169, 169)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
CYAN = (0, 204, 204)
PINK = (255, 105, 180)
percentChanceForWall = 20
actualPercentOfWalls = 0
weight = 1

grid = [[Node(i, j) for j in range(GRID_X)] for i in range(GRID_Y)]

S = grid[0][GRID_Y - 1]
G = grid[GRID_X - 1][0]

for y in range(GRID_X):
    for x in range(GRID_Y):
        if grid[x][y] != S and grid[x][y] != G:
            if randint(1, 100) <= percentChanceForWall:
                grid[x][y].setObstacle()
                actualPercentOfWalls += 1
        if north(grid, x, y, GRID_Y):
            grid[x][y].children.append(north(grid, x, y, GRID_Y))
        if south(grid, x, y, GRID_Y):
            grid[x][y].children.append(south(grid, x, y, GRID_Y))
        if west(grid, x, y, GRID_X):
            grid[x][y].children.append(west(grid, x, y, GRID_X))
        if east(grid, x, y, GRID_X):
            grid[x][y].children.append(east(grid, x, y, GRID_X))
        if northEast(grid, x, y, GRID_X, GRID_Y):
            grid[x][y].children.append(northEast(grid, x, y, GRID_X, GRID_Y))
        if northWest(grid, x, y, GRID_X, GRID_Y):
            grid[x][y].children.append(northWest(grid, x, y, GRID_X, GRID_Y))
        if southEast(grid, x, y, GRID_X, GRID_Y):
            grid[x][y].children.append(southEast(grid, x, y, GRID_X, GRID_Y))
        if southWest(grid, x, y, GRID_X, GRID_Y):
            grid[x][y].children.append(southWest(grid, x, y, GRID_X, GRID_Y))

for i in range(19, 79):
    grid[i][19].setObstacle()

for i in range(19, 79):
    grid[79][i].setObstacle()

for y in range(GRID_X):
    for x in range(GRID_Y):
        if grid[x][y].isObstacle:
            drawRect(BLACK, x, y)
        else:
            drawRect(GRAY, x, y)
        if x == 0 and y == GRID_Y - 1:
            drawRect(GREEN, x, y)
        if x == GRID_X - 1 and y == 0:
            drawRect(RED, x, y)
pygame.display.flip()
startTime = time.time()
path = araStar(S, G, weight)
print('It took %s seconds to run' % str(round(time.time() - startTime, 3)))
if path:
    drawPath(path, PINK)
    print(path[-1].G)
    drawRect(GREEN, S.x, S.y)
    drawRect(RED, G.x, G.y)
    pygame.display.update()
else:
    print('No path from start to goal.')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

