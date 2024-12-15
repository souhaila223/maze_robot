import heapq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def display_maze_graphically(maze, path):
    """Display the maze and the solution path graphically."""
    # Define colors
    color_map = {
        "S": "blue",   # Start point
        "E": "green",  # End point
        "#": "grey",  # Obstacle
        " ": "white",  # Empty path
        "*": "red"     # Solution path
    }

    rows, cols = len(maze), len(maze[0])
    grid = np.zeros((rows, cols, 3))  # RGB grid for visualization

    for i in range(rows):
        for j in range(cols):
            if (i, j) == start:
                grid[i, j] = [0.53, 0.81, 0.92]  # Sky blue for start point
            elif (i, j) == end:
                grid[i, j] = [0, 1, 0]  # Green for end point
            elif (i, j) in path:
                grid[i, j] = [0.6, 1.0, 0.6]  # Mint green for solution path
            elif maze[i][j] in color_map:
                color = color_map[maze[i][j]]
                if color == "grey":
                    grid[i, j] = [0.5, 0.5, 0.5]
                elif color == "white":
                    grid[i, j] = [1, 1, 1]


    plt.imshow(grid, interpolation='nearest')
    plt.axis('off')
    plt.title("Maze Solution")
    plt.savefig("mygraph.png")

def heuristic(a, b):
    """Calculate Manhattan distance as the heuristic."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(maze, start, end):
    """Perform A* search to find the shortest path in the maze."""
    rows, cols = len(maze), len(maze[0])
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and maze[neighbor[0]][neighbor[1]] != "#":
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None  # No path found

if __name__ == "__main__":
    maze = [
        ["S", " ", "#", " ", " ", "#", " ", " ", " ", "E"],
        ["#", " ", "#", " ", "#", "#", "#", "#", " ", "#"],
        [" ", " ", " ", " ", " ", "#", " ", " ", " ", "#"],
        [" ", "#", "#", "#", " ", "#", "#", " ", "#", "#"],
        [" ", "#", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", "#", " ", "#", "#", "#", " ", "#", " ", "#"],
        [" ", " ", " ", "#", " ", " ", " ", " ", " ", " "],
        ["#", "#", "#", "#", " ", "#", "#", "#", "#", " "]
    ]

    start, end = None, None
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == "S":
                start = (i, j)
            elif maze[i][j] == "E":
                end = (i, j)

    if start is None or end is None:
        print("Maze must have a start (S) and an exit (E).")
    else:
        path = a_star_search(maze, start, end)
        if path:
            for x, y in path:
                if maze[x][y] not in ("S", "E"):
                    maze[x][y] = "*"

            display_maze_graphically(maze, path)
        else:
            print("No path found!")
