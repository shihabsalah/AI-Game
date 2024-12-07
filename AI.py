from queue import Queue
import heapq

class AI:
    def __init__(self, start_pos, end_pos):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.path = []

    def bfs(self, maze):
        rows, cols = len(maze), len(maze[0])
        queue = Queue()
        queue.put(self.start_pos)
        visited = set()
        visited.add(self.start_pos)
        parent = {}

        while not queue.empty():
            x, y = queue.get()
            if (x, y) == self.end_pos:
                return self.reconstruct_path(parent)

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < cols and 0 <= ny < rows and maze[ny][nx] == 0 and (nx, ny) not in visited:
                    queue.put((nx, ny))
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)

        return []

    def dfs(self, maze):
        rows, cols = len(maze), len(maze[0])
        stack = [self.start_pos]
        visited = set()
        parent = {}

        while stack:
            x, y = stack.pop()
            if (x, y) == self.end_pos:
                return self.reconstruct_path(parent)

            if (x, y) not in visited:
                visited.add((x, y))
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < cols and 0 <= ny < rows and maze[ny][nx] == 0 and (nx, ny) not in visited:
                        stack.append((nx, ny))
                        parent[(nx, ny)] = (x, y)

        return []

    def a_star(self, maze):
        rows, cols = len(maze), len(maze[0])
        open_set = []
        heapq.heappush(open_set, (0, self.start_pos))
        g_score = {self.start_pos: 0}
        f_score = {self.start_pos: self.heuristic(self.start_pos)}
        parent = {}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == self.end_pos:
                return self.reconstruct_path(parent)

            x, y = current
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < cols and 0 <= ny < rows and maze[ny][nx] == 0:
                    tentative_g_score = g_score[current] + 1
                    if (nx, ny) not in g_score or tentative_g_score < g_score[(nx, ny)]:
                        g_score[(nx, ny)] = tentative_g_score
                        f_score[(nx, ny)] = tentative_g_score + self.heuristic((nx, ny))
                        heapq.heappush(open_set, (f_score[(nx, ny)], (nx, ny)))
                        parent[(nx, ny)] = current

        return []

    def heuristic(self, pos):
        # Manhattan distance
        return abs(pos[0] - self.end_pos[0]) + abs(pos[1] - self.end_pos[1])

    def reconstruct_path(self, parent):
        path = []
        current = self.end_pos
        while current in parent:
            path.append(current)
            current = parent[current]
        path.reverse()
        return path
