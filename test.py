import random
import math
import numpy as np

def poisson_disc_sampling(width, height, radius, k):
    GRID_SIZE = radius / math.sqrt(2)
    cols, rows = int(width / GRID_SIZE) + 1, int(height / GRID_SIZE) + 1

    def initialize_grid():
        return np.full((cols, rows), None, dtype=object)

    def distance(p1, p2):
        return np.hypot(p1[0] - p2[0], p1[1] - p2[1])

    def generate_point_around(point):
        r = radius * (random.random() + 1)
        angle = 2 * math.pi * random.random()
        new_x = point[0] + r * math.cos(angle)
        new_y = point[1] + r * math.sin(angle)
        return new_x, new_y

    def in_bounds(point):
        return 0 <= point[0] < width and 0 <= point[1] < height

    def fits(point):
        col = int(point[0] / GRID_SIZE)
        row = int(point[1] / GRID_SIZE)
        for i in range(max(col - 2, 0), min(col + 3, cols)):
            for j in range(max(row - 2, 0), min(row + 3, rows)):
                neighbor = grid[i, j]
                if neighbor is not None and distance(point, neighbor) < radius:
                    return False
        return True

    def restart_simulation(start_point):
        nonlocal grid, active, points
        grid = initialize_grid()
        points = [start_point]
        active = [start_point]
        col = int(start_point[0] / GRID_SIZE)
        row = int(start_point[1] / GRID_SIZE)
        grid[col, row] = start_point

    # Create a grid to store points
    grid = initialize_grid()

    # List to store active points
    active = []
    points = []

    # Initialize with a random point
    initial_point = (random.uniform(0, width), random.uniform(0, height))
    restart_simulation(initial_point)

    # Main loop
    while active:
        rand_index = random.randint(0, len(active) - 1)
        point = active[rand_index]
        found = False

        for _ in range(k):
            new_point = generate_point_around(point)
            if in_bounds(new_point) and fits(new_point):
                points.append(new_point)
                active.append(new_point)
                col = int(new_point[0] / GRID_SIZE)
                row = int(new_point[1] / GRID_SIZE)
                grid[col][row] = new_point
                found = True
                break

        if not found:
            active.pop(rand_index)
            # Create a 2D numpy array representation
    matrix = np.zeros((height, width), dtype=int)
    for p in points:
        x, y = int(p[0]), int(p[1])
        matrix[y, x] = 1

    return matrix
def visualize_matrix(matrix):
    import matplotlib.pyplot as plt
    plt.imshow(matrix, cmap='Greys', interpolation='none')
    plt.show()
# Example usage
a = poisson_disc_sampling(128, 128, 2, 10)
visualize_matrix(a)
[print(a[r]) for r in range(a.shape[0])]
