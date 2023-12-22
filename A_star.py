from warnings import warn
import copy


class Node():
    """ A node class for A* Pathfinding. """

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __repr__(self):
        return f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"

    def __eq__(self, other):
        return self.position == other.position


def maze_path(maze, path):
    """ return Maze and Path from start to end """

    new_maze = copy.deepcopy(maze)
    for step in path:
        new_maze[step[0]][step[1]] = 2

    for row in new_maze:
        line = []
        for col in row:
            if col == 1:
                line.append("\u2593")
            elif col == 0:
                line.append(" ")
            elif col == 2:
                line.append("+")
        print("".join(line))


def return_path(current_node):
    """ return Finded path from start to end. """
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    # Return reversed path
    return path[::-1]


def astar(maze, start, end, allow_diagonal_movement=False):
    """
        Returns a list of tuples as a path
        from the given start to the given end in the given maze
    """

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Adding a stop condition
    outer_iterations = 0
    max_iterations = (len(maze[0]) * len(maze))

    adjacent_squares = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    if allow_diagonal_movement:
        adjacent_squares = [(0, -1), (0, 1), (-1, 0), (1, 0),
                            (-1, -1), (-1, 1), (1, -1), (1, 1)]

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:
        outer_iterations += 1

        if outer_iterations > max_iterations:
            # if we hit this point return the path such as it is
            # it will not contain the destination
            warn("giving up on pathfinding too many iterations ::  ")
            return (None, )

        # Get the current node (a node with smallest f)
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            return return_path(current_node)

        # Generate children
        children = []
        for new_position in adjacent_squares:
            # Get node position
            node_position = (current_node.position[0] + new_position[0],
                             current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) \
                or node_position[0] < 0 \
                    or node_position[1] > (len(maze[len(maze)-1]) - 1) \
                    or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            # Child is on the closed list
            _continue = False
            for closed_child in closed_list:
                if closed_child == child:
                    _continue = True
            if _continue:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0])**2) + \
                ((child.position[1] - end_node.position[1])**2)
            child.f = child.g + child.h

            # Child is already in the open list
            _continue = False
            for open_node in open_list:
                if child.position == open_node.position and \
                        child.g > open_node.g:
                    _continue = True
            if _continue:
                continue

            # Add the child to the open list
            open_list.append(child)

    warn("Couldn't get a path to destination")
    return None


def main():
    """
        Main method.
        Initiate maze and run A*.
    """
    maze = [[0, 0, 0, 0, 1, 0, 1, 0, 0, 0]*2,
            [1, 1, 1, 0, 1, 1, 0, 0, 1, 0]*2,
            [1, 0, 0, 0, 1, 0, 0, 1, 0, 0]*2,
            [1, 0, 0, 1, 1, 0, 1, 1, 0, 1]*2,
            [1, 0, 1, 0, 1, 0, 1, 1, 0, 1]*2,
            [1, 0, 0, 0, 1, 0, 1, 0, 0, 1]*2,
            [1, 0, 1, 0, 1, 0, 1, 0, 0, 1]*2,
            [1, 0, 0, 0, 1, 0, 1, 0, 0, 1]*2,
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 0]*2,
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0]*2]

    from maze_generator import make_maze, printMaze
    maze = make_maze(25, 100)

    start = (0, 0)
    end = (len(maze)-1, len(maze[0])-1)

    path = astar(maze=maze, start=start, end=end,
                 allow_diagonal_movement=False)

    if path is not None:
        # print(maze_path(maze, path))
        printMaze(maze, path=path)
        print(path)


if __name__ == '__main__':
    main()
