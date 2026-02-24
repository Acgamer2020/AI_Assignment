import random
import heapq


class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[random.choice([True, False]) for _ in range(height)]
                     for _ in range(width)]

    def is_dirty(self, x, y):
        return self.grid[x][y]

    def clean(self, x, y):
        self.grid[x][y] = False

    def any_dirt_left(self):
        return any(self.grid[x][y]
                   for x in range(self.width)
                   for y in range(self.height))

    def display(self, agent_x, agent_y):
        for y in range(self.height):
            for x in range(self.width):
                if x == agent_x and y == agent_y:
                    print("A", end=" ")
                elif self.grid[x][y]:
                    print("*", end=" ")
                else:
                    print(".", end=" ")
            print()
        print()


class GoalBasedAgent:
    def __init__(self, start_x, start_y):
        self.x = start_x
        self.y = start_y

    def act(self, grid):
        # If standing on dirt then clean
        if grid.is_dirty(self.x, self.y):
            grid.clean(self.x, self.y)
            print(f"Cleaning at ({self.x},{self.y})")
            return

        goal = self.find_nearest_dirt(grid)
        if goal is None:
            return

        path = self.a_star(grid, (self.x, self.y), goal)

        if path and len(path) > 1:
            self.x, self.y = path[1]
            print(f"Moving to ({self.x},{self.y})")

    def find_nearest_dirt(self, grid):
        min_distance = float("inf")
        target = None

        for x in range(grid.width):
            for y in range(grid.height):
                if grid.is_dirty(x, y):
                    dist = abs(x - self.x) + abs(y - self.y)
                    if dist < min_distance:
                        min_distance = dist
                        target = (x, y)

        return target

    def a_star(self, grid, start, goal):
        open_list = []
        heapq.heappush(open_list, (0, start))

        came_from = {}
        g_score = {start: 0}

        while open_list:
            _, current = heapq.heappop(open_list)

            if current == goal:
                return self.reconstruct_path(came_from, current)

            for neighbor in self.get_neighbors(grid, current):
                tentative_g = g_score[current] + 1

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + self.heuristic(neighbor, goal)
                    heapq.heappush(open_list, (f_score, neighbor))

        return None

    def reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.insert(0, current)
        return path

    def get_neighbors(self, grid, pos):
        x, y = pos
        neighbors = []

        moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < grid.width and 0 <= ny < grid.height:
                neighbors.append((nx, ny))

        return neighbors

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])


def main():
    grid = Grid(5, 4)
    agent = GoalBasedAgent(0, 0)

    steps = 0
    while grid.any_dirt_left() and steps < 100:
        print(f"Step {steps}")
        grid.display(agent.x, agent.y)
        agent.act(grid)
        steps += 1

    print("Finished cleaning!")


if __name__ == "__main__":
    main()