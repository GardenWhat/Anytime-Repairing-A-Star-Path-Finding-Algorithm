import time
import os
import pygame
import utils
import node

pygame.init()

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
w = 200


def araStar(start, goal, weight):
    incumbent = []
    pathCost = 100000000000000000

    weightDelta = int(weight / 10)
    nonWeightedRun = False

    while weight > 0:
        newSolution = improvedSolution(start, goal, weight, pathCost)

        if newSolution:
            pathCost = newSolution[-1].G
            incumbent = newSolution
            utils.drawPath(incumbent, utils.randomColor(), start, goal, screen, MARGIN, GRID_SIZE)
            time.sleep(.5)

        weight = weight - weightDelta
        if weight < 0 and not nonWeightedRun:
            weight = 1
            nonWeightedRun = True
    return incumbent


def improvedSolution(start, goal, weight, pathCost):
    openList = set()
    closedList = set()

    current = start
    current.G = 0
    current.H = utils.ED(current, goal)

    openList.add(current)

    while openList:

        current = min(openList, key=lambda o: o.G + (weight * o.H))

        openList.remove(current)
        closedList.add(current)

        # exits function if estimated travel is more than best path cost
        if pathCost <= current.G + (weight * current.H):
            # pathCost is proven to be w-admissible
            return None

        if current == goal:
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
            path.append(current)
            return path[::-1]

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


def main():
    grid = [[node.Node(i, j) for j in range(GRID_X)] for i in range(GRID_Y)]

    start = grid[0][GRID_Y - 1]
    goal = grid[GRID_X - 1][0]

    grid = utils.setChildren(GRID_X, GRID_Y, grid, percentChanceForWall, actualPercentOfWalls, start, goal)
    utils.drawGrid(GRID_X, GRID_Y, grid, screen, MARGIN, GRID_SIZE, BLACK, GRAY, GREEN, RED)

    pygame.display.flip()
    startTime = time.time()
    path = araStar(start, goal, w)
    print('It took %s seconds to run' % str(round(time.time() - startTime, 3)))
    if path:
        utils.drawPath(path, PINK, start, goal, screen, MARGIN, GRID_SIZE)
        print(f"Finished with a weight of {round(path[-1].G, 3)}")
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


if __name__ == "__main__":
    main()
