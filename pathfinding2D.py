

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0
        self.p = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    """Returns a list of tuples as a Path from the given start to the given end in the given maze"""

    # Create start and end node
    StartNode = Node(None, start)
    StartNode.g = StartNode.h = StartNode.f = 0
    EndNode = Node(None, end)
    EndNode.g = EndNode.h = EndNode.f = 0

    # Initialize both open and closed list
    OpenList = []
    ClosedList = []

    # Add the start node
    OpenList.append(StartNode)

    # Loop until you find the end
    while len(OpenList) > 0:

        # Get the Current node
        CurrentNode = OpenList[0]
        CurrentIndex = 0
        for index, Item in enumerate(OpenList):
            if Item.f < CurrentNode.f:
                CurrentNode = Item
                CurrentIndex = index

        # Pop current off open list, add to closed li   st
        OpenList.pop(CurrentIndex)
        ClosedList.append(CurrentNode)

        # Found the goal
        if CurrentNode == EndNode:
            Path = []
            Current = CurrentNode
            while Current is not None:
                Path.append(Current.position)
                Current = Current.parent
            return Path[::-1] # Return reversed Path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            NodePosition = (CurrentNode.position[0] + new_position[0], CurrentNode.position[1] + new_position[1])

            # Make sure within range
            if NodePosition[0] > (len(maze) - 1) or NodePosition[0] < 0 or NodePosition[1] > (len(maze[len(maze)-1]) -1) or NodePosition[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[NodePosition[0]][NodePosition[1]] == -1:
                continue

            # Create new node
            new_node = Node(CurrentNode, NodePosition)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for ClosedChild in ClosedList:
                if child == ClosedChild:
                    continue

            # Create the f, g, and h values
            child.g = CurrentNode.g + 1
            child.h = ((child.position[0] - EndNode.position[0]) ** 2) + ((child.position[1] - EndNode.position[1]) ** 2)
            child.p = (maze[child.position[0]][child.position[1]])
            print(child.g)
            print(child.h)
            child.f = child.g + child.h +child.p

            # Child is already in the open list
            for OpenNode in OpenList:
                if child == OpenNode and child.g > OpenNode.g:
                    continue

            # Add the child to the open list
            OpenList.append(child)


def main():

    maze = [[0, 0, 0, 0, -1, 0, 0, 0, 0, 0],
            [0, 13, 0, 0, -1, 0, 0, 0, 0, 0],
            [0, 0, 0, 3, -1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, -1, 0, 0, 0, 0, 0],
            [0, 8, 0, 0, -1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, -1, 0.5, 0, 0, 0, 0],
            [0, 0, 0, 0, -1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, -1, 0, 0, 0, 0, 0],
            [0, 3, 0, 0, -1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    start = (0, 0)
    end = (7, 6)

    Path = astar(maze, start, end)
    print(Path)


if __name__ == '__main__':
    main()
