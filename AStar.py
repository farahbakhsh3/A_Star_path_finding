
class Node:
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


class AStar:
    def __init__(self, grid, start, end):
        self.maze = grid
        self.start = start
        self.end = end

    @staticmethod
    def return_path(current_node):
        """ return Finded path from start to end. """
        path = []
        current = current_node
        while current is not None:
            path.append(current.position)
            current = current.parent
        # Return reversed path
        return path[::-1]

    def astar(self, allow_diagonal_movement):
        """
            Returns a list of tuples as a path
            from the given start to the given end in the given maze
        """

        # Create start and end node
        start_node = Node(None, self.start)
        start_node.g = 0
        start_node.h = 0
        start_node.f = 0

        end_node = Node(None, self.end)
        end_node.g = 0
        end_node.h = 0
        end_node.f = 0

        # Adding a stop condition
        outer_iterations = 0
        max_iterations = (len(self.maze[0]) * len(self.maze)) ** 2

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
                print("giving up on pathfinding too many iterations ::  ")
                return None

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
                return self.return_path(current_node)

            # Generate children
            children = []
            for new_position in adjacent_squares:
                # Get node position
                node_position = (current_node.position[0] + new_position[0],
                                 current_node.position[1] + new_position[1])

                # Make sure within range
                if (node_position[0] > (len(self.maze) - 1) or
                        node_position[0] < 0 or
                        node_position[1] > (len(self.maze[len(self.maze) - 1]) - 1) or
                        node_position[1] < 0):
                    continue

                # Make sure walkable terrain
                if self.maze[node_position[0]][node_position[1]] != 0:
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
                child.h = abs(child.position[0] - end_node.position[0]) + abs(child.position[1] - end_node.position[1])
                child.f = child.g + child.h

                # Child is already in the open list
                _continue = False
                for open_node in open_list:
                    if (child.position == open_node.position
                            and child.g >= open_node.g):
                        _continue = True
                if _continue:
                    continue

                # Add the child to the open list
                open_list.append(child)

        print("Couldn't get a path to destination")
        return None


def main():
    """
        Main method.
        Initiate maze and run A*.
    """

    maze = [[0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    start = (0, 0)
    end = (len(maze) - 1, len(maze[0]) - 1)

    astar = AStar(maze, start, end)
    path = astar.astar(allow_diagonal_movement=False)

    if path is not None:
        print(path)


if __name__ == '__main__':
    main()
