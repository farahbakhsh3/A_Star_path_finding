# Maze generator -- Randomized Prim Algorithm

# Imports
import random
from colorama import init
from colorama import Fore


# Init variables
wall = 1
cell = 0
unvisited = 'u'
height = 0
width = 0
maze = []


# Functions
def printMaze(maze, path=None):
    height = len(maze)
    width = len(maze[0])
    if path is not None:
        for step in path:
            maze[step[0]][step[1]] = 2
           
    for i in range(0, height):
        for j in range(0, width):
            if (maze[i][j] == unvisited):
                print(Fore.WHITE + str(maze[i][j]), end=" ")
            elif (maze[i][j] == cell):
                print(Fore.GREEN + "\u2592", end="")
            elif (maze[i][j] == wall):
                print(Fore.BLACK + "\u2592", end="")
            else:
                print(Fore.RED + "\u2592", end="")

        print()


# Find number of surrounding cells
def surroundingCells(rand_wall):
    s_cells = 0
    if (maze[rand_wall[0]-1][rand_wall[1]] == cell):
        s_cells += 1
    if (maze[rand_wall[0]+1][rand_wall[1]] == cell):
        s_cells += 1
    if (maze[rand_wall[0]][rand_wall[1]-1] == cell):
        s_cells += 1
    if (maze[rand_wall[0]][rand_wall[1]+1] == cell):
        s_cells += 1

    return s_cells


def make_maze(h, w):
    # Main code
    global height
    height = h
    global width
    width = w

    # Initialize colorama
    init()

    # Denote all cells as unvisited
    for i in range(0, height):
        line = []
        for j in range(0, width):
            line.append(unvisited)
        maze.append(line)

    # Randomize starting point and set it a cell
    starting_height = 0  # int(random.random()*height)
    starting_width = 0  # int(random.random()*width)
    if (starting_height == 0):
        starting_height += 1
    if (starting_height == height-1):
        starting_height -= 1
    if (starting_width == 0):
        starting_width += 1
    if (starting_width == width-1):
        starting_width -= 1

    # Mark it as cell and add surrounding walls to the list
    maze[starting_height][starting_width] = cell
    walls = []
    walls.append([starting_height - 1, starting_width])
    walls.append([starting_height, starting_width - 1])
    walls.append([starting_height, starting_width + 1])
    walls.append([starting_height + 1, starting_width])

    # Denote walls in maze
    maze[starting_height-1][starting_width] = wall
    maze[starting_height][starting_width - 1] = wall
    maze[starting_height][starting_width + 1] = wall
    maze[starting_height + 1][starting_width] = wall

    while (walls):
        # Pick a random wall
        rand_wall = walls[int(random.random()*len(walls))-1]

        # Check if it is a left wall
        if (rand_wall[1] != 0):
            if (maze[rand_wall[0]][rand_wall[1]-1] == unvisited and maze[rand_wall[0]][rand_wall[1]+1] == cell):
                # Find the number of surrounding cells
                s_cells = surroundingCells(rand_wall)

                if (s_cells < 2):
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = cell

                    # Mark the new walls
                    # Upper cell
                    if (rand_wall[0] != 0):
                        if (maze[rand_wall[0]-1][rand_wall[1]] != cell):
                            maze[rand_wall[0]-1][rand_wall[1]] = wall
                        if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0]-1, rand_wall[1]])

                    # Bottom cell
                    if (rand_wall[0] != height-1):
                        if (maze[rand_wall[0]+1][rand_wall[1]] != cell):
                            maze[rand_wall[0]+1][rand_wall[1]] = wall
                        if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0]+1, rand_wall[1]])

                    # Leftmost cell
                    if (rand_wall[1] != 0):
                        if (maze[rand_wall[0]][rand_wall[1]-1] != cell):
                            maze[rand_wall[0]][rand_wall[1]-1] = wall
                        if ([rand_wall[0], rand_wall[1]-1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1]-1])

                # Delete wall
                for _wall in walls:
                    if (_wall[0] == rand_wall[0] and _wall[1] == rand_wall[1]):
                        walls.remove(_wall)

                continue

        # Check if it is an upper wall
        if (rand_wall[0] != 0):
            if (maze[rand_wall[0]-1][rand_wall[1]] == unvisited and maze[rand_wall[0]+1][rand_wall[1]] == cell):

                s_cells = surroundingCells(rand_wall)
                if (s_cells < 2):
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = cell

                    # Mark the new walls
                    # Upper cell
                    if (rand_wall[0] != 0):
                        if (maze[rand_wall[0]-1][rand_wall[1]] != cell):
                            maze[rand_wall[0]-1][rand_wall[1]] = wall
                        if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0]-1, rand_wall[1]])

                    # Leftmost cell
                    if (rand_wall[1] != 0):
                        if (maze[rand_wall[0]][rand_wall[1]-1] != cell):
                            maze[rand_wall[0]][rand_wall[1]-1] = wall
                        if ([rand_wall[0], rand_wall[1]-1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1]-1])

                    # Rightmost cell
                    if (rand_wall[1] != width-1):
                        if (maze[rand_wall[0]][rand_wall[1]+1] != cell):
                            maze[rand_wall[0]][rand_wall[1]+1] = wall
                        if ([rand_wall[0], rand_wall[1]+1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1]+1])

                # Delete wall
                for _wall in walls:
                    if (_wall[0] == rand_wall[0] and _wall[1] == rand_wall[1]):
                        walls.remove(_wall)

                continue

        # Check the bottom wall
        if (rand_wall[0] != height-1):
            if (maze[rand_wall[0]+1][rand_wall[1]] == unvisited and maze[rand_wall[0]-1][rand_wall[1]] == cell):

                s_cells = surroundingCells(rand_wall)
                if (s_cells < 2):
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = cell

                    # Mark the new walls
                    if (rand_wall[0] != height-1):
                        if (maze[rand_wall[0]+1][rand_wall[1]] != cell):
                            maze[rand_wall[0]+1][rand_wall[1]] = wall
                        if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0]+1, rand_wall[1]])
                    if (rand_wall[1] != 0):
                        if (maze[rand_wall[0]][rand_wall[1]-1] != cell):
                            maze[rand_wall[0]][rand_wall[1]-1] = wall
                        if ([rand_wall[0], rand_wall[1]-1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1]-1])
                    if (rand_wall[1] != width-1):
                        if (maze[rand_wall[0]][rand_wall[1]+1] != cell):
                            maze[rand_wall[0]][rand_wall[1]+1] = wall
                        if ([rand_wall[0], rand_wall[1]+1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1]+1])

                # Delete wall
                for _wall in walls:
                    if (_wall[0] == rand_wall[0] and _wall[1] == rand_wall[1]):
                        walls.remove(_wall)

                continue

        # Check the right wall
        if (rand_wall[1] != width-1):
            if (maze[rand_wall[0]][rand_wall[1]+1] == unvisited and maze[rand_wall[0]][rand_wall[1]-1] == cell):

                s_cells = surroundingCells(rand_wall)
                if (s_cells < 2):
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = cell

                    # Mark the new walls
                    if (rand_wall[1] != width-1):
                        if (maze[rand_wall[0]][rand_wall[1]+1] != cell):
                            maze[rand_wall[0]][rand_wall[1]+1] = wall
                        if ([rand_wall[0], rand_wall[1]+1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1]+1])
                    if (rand_wall[0] != height-1):
                        if (maze[rand_wall[0]+1][rand_wall[1]] != cell):
                            maze[rand_wall[0]+1][rand_wall[1]] = wall
                        if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0]+1, rand_wall[1]])
                    if (rand_wall[0] != 0):
                        if (maze[rand_wall[0]-1][rand_wall[1]] != cell):
                            maze[rand_wall[0]-1][rand_wall[1]] = wall
                        if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0]-1, rand_wall[1]])

                # Delete wall
                for _wall in walls:
                    if (_wall[0] == rand_wall[0] and _wall[1] == rand_wall[1]):
                        walls.remove(_wall)

                continue

        # Delete the wall from the list anyway
        for _wall in walls:
            if (_wall[0] == rand_wall[0] and _wall[1] == rand_wall[1]):
                walls.remove(_wall)

    # Mark the remaining unvisited cells as walls
    for i in range(0, height):
        for j in range(0, width):
            if (maze[i][j] == unvisited):
                maze[i][j] = wall

    # Set entrance and exit
    for i in range(0, width):
        maze[0][i] = cell
        if (maze[1][i] == cell):
            break

    for i in range(width-1, 0, -1):
        maze[height-1][i] = cell
        if (maze[height-2][i] == cell):
            break

    # Print final maze
    # printMaze(maze)
    return maze


if __name__ == '__main__':
    maze_ = make_maze(10, 17)
    printMaze(maze_)
    print(maze_)