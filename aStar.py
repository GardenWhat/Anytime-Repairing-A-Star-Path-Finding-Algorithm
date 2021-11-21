import time
import os
import pygame
import utils
import node

pygame.init()


def araStar(start, goal, weight):
    openList = set()
    closedList = set()
    incumbent = []
    # s
    current = start

    current.G = 0

    # sets the start nodes heuristic
    current.H = utils.ED(current, goal)

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
            utils.drawPath(incumbent, utils.randomColor(), start, goal, screen, MARGIN, GRID_SIZE)
            time.sleep(.5)
        else:
            return incumbent

        # weight = weight - weightDelta

        for child in current.children:
            if current.G + utils.ED(current, child) < child.G:
                if child.isObstacle:
                    continue
                child.parent = current
                child.G = current.G + child.cost()
                child.H = utils.ED(child, goal)

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

            utils.drawRect(CYAN, node.x, node.y, screen, MARGIN, GRID_SIZE)
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
                    node.H = utils.ED(node, goal)
                else:
                    path = []
                    while node.parent:
                        node = node.parent
                        path.append(node)
                    path.append(node)
                    return path[::-1]
                openList.add(node)
    return None





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
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
CYAN = (0, 204, 204)
PINK = (255, 105, 180)
percentChanceForWall = 30
actualPercentOfWalls = 0
weight = 2

grid = [[node.Node(i, j) for j in range(GRID_X)] for i in range(GRID_Y)]

start = grid[0][GRID_Y - 1]
goal = grid[GRID_X - 1][0]

grid = utils.setChildren(GRID_X, GRID_Y, grid, percentChanceForWall, actualPercentOfWalls, start, goal)



# for i in range(19, 79):
#     grid[i][19].setObstacle()
#
# for i in range(19, 79):
#     grid[79][i].setObstacle()

for y in range(GRID_X):
    for x in range(GRID_Y):
        if grid[x][y].isObstacle:
            utils.drawRect(BLACK, x, y, screen, MARGIN, GRID_SIZE)
        else:
            utils.drawRect(GRAY, x, y, screen, MARGIN, GRID_SIZE)
        if x == 0 and y == GRID_Y - 1:
            utils.drawRect(GREEN, x, y, screen, MARGIN, GRID_SIZE)
        if x == GRID_X - 1 and y == 0:
            utils.drawRect(RED, x, y, screen, MARGIN, GRID_SIZE)
pygame.display.flip()
startTime = time.time()
path = araStar(start, goal, weight)
print('It took %s seconds to run' % str(round(time.time() - startTime, 3)))
if path:
    utils.drawPath(path, PINK, start, goal, screen, MARGIN, GRID_SIZE)
    print(path[-1].G)
    utils.drawRect(GREEN, start.x, start.y, screen, MARGIN, GRID_SIZE)
    utils.drawRect(RED, goal.x, goal.y, screen, MARGIN, GRID_SIZE)
    pygame.display.update()
else:
    print('No path from start to goal.')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

