from queue import Queue
import heapq
from queue import Queue
import heapq
from Maze import Maze

class AI:
    def __init__(self, start_position, goal_position):
        """
        Initialize the AI with starting and goal positions.
        
        :param start_position: Tuple (x, y) for the starting position.
        :param goal_position: Tuple (x, y) for the goal position.
        """
        self.start_position = start_position
        self.goal_position = goal_position

    # ------------------------------
    # Breadth-First Search (BFS)
    # ------------------------------
    def bfs(self, start_position, maze):
        if self._is_path_blocked(start_position, maze):
            return []
        if not self.validate_connectivity(maze):
            return []

        """
        Perform Breadth-First Search (BFS) to find the shortest path in an unweighted maze.
        
        BFS explores all possible paths layer by layer, ensuring the shortest path is found.
        
        :param maze: 2D list where 0 = open path, 1 = wall.
        :return: List of positions representing the shortest path from start to goal.
        """
        rows, cols = len(maze), len(maze[0])
        queue = Queue()
        queue.put(start_position)  # Queue holds positions to explore
        visited = set()                # Keep track of visited positions
        visited.add(start_position)
        parent_map = {}                # Map each position to its parent for path reconstruction

        while not queue.empty():
            current_position = queue.get()

            # Check if we've reached the goal
            if current_position == self.goal_position:
                return self._reconstruct_path(parent_map)

            # Explore all valid neighbors
            for neighbor in self._get_neighbors(current_position, maze, rows, cols):
                if neighbor not in visited:
                    queue.put(neighbor)
                    visited.add(neighbor)
                    parent_map[neighbor] = current_position  # Track how we reached this position

        return []  # No path found

    # ------------------------------
    # Depth-First Search (DFS)
    # ------------------------------
    def dfs(self, start_position, maze):
        if self._is_path_blocked(start_position, maze):
            return []
        if not self.validate_connectivity(maze):
            return []
        """
        Perform Depth-First Search (DFS) to find a path in the maze.
        
        DFS explores as far as possible along one path before backtracking.
        
        :param maze: 2D list where 0 = open path, 1 = wall.
        :return: List of positions representing a path from start to goal.
        """
        rows, cols = len(maze), len(maze[0])
        stack = [start_position]  # Stack for DFS
        visited = set()               # Keep track of visited positions
        parent_map = {}               # Map each position to its parent for path reconstruction

        while stack:    # Continue until all paths are explored
            current_position = stack.pop()
            # Check if we've reached the goal
            if current_position == self.goal_position:
                return self._reconstruct_path(parent_map)

            # Explore all valid neighbors
            if current_position not in visited:
                visited.add(current_position)
                for neighbor in self._get_neighbors(current_position, maze, rows, cols):
                    if neighbor not in visited:
                        stack.append(neighbor)
                        parent_map[neighbor] = current_position  # Track how we reached this position
        return []  # No path found

    # ------------------------------
    # A* Search
    # ------------------------------
    def a_star(self, start_position, maze):
        if self._is_path_blocked(start_position, maze):
            return []
        if not self.validate_connectivity(maze):
            return []
        """
        Perform A* Search to find the optimal path using a heuristic.
        
        A* combines the cost of the path so far (g) and an estimate to the goal (h).
        
        :param maze: 2D list where 0 = open path, 1 = wall.
        :return: List of positions representing the optimal path from start to goal.
        """
        rows, cols = len(maze), len(maze[0])
        open_set = []  # Priority queue for positions to explore
        heapq.heappush(open_set, (0, start_position))  # (priority, position)
        g_cost = {start_position: 0}  # Cost of the path from start to a position
        f_cost = {start_position: self._heuristic(start_position)}  # Total estimated cost
        parent_map = {}  # Map each position to its parent for path reconstruction

        while open_set:
            _, current_position = heapq.heappop(open_set)

            # Check if we've reached the goal
            if current_position == self.goal_position:
                return self._reconstruct_path(parent_map)

            # Explore all valid neighbors
            for neighbor in self._get_neighbors(current_position, maze, rows, cols):
                tentative_g_cost = g_cost[current_position] + 1  # Distance to neighbor
                if neighbor not in g_cost or tentative_g_cost < g_cost[neighbor]:
                    # Update costs and priority queue
                    g_cost[neighbor] = tentative_g_cost
                    f_cost[neighbor] = tentative_g_cost + self._heuristic(neighbor)
                    heapq.heappush(open_set, (f_cost[neighbor], neighbor))
                    parent_map[neighbor] = current_position  # Track how we reached this position

        return []  # No path found

    # ------------------------------
    # Utility Functions
    # ------------------------------
    def _get_neighbors(self, position, maze, rows, cols):
        """
        Get all valid neighbors (adjacent positions) for a given position.
        
        :param position: Current position (x, y).
        :param maze: 2D list representing the maze.
        :param rows: Number of rows in the maze.
        :param cols: Number of columns in the maze.
        :return: List of valid neighbors as (x, y) tuples.
        """
        x, y = position
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows and maze[ny][nx] == 0:
                neighbors.append((nx, ny))
        return neighbors

    def _heuristic(self, position):
        """
        Calculate the Manhattan distance heuristic.
        
        :param position: Current position (x, y).
        :return: Estimated cost (Manhattan distance) to reach the goal.
        """
        return abs(position[0] - self.goal_position[0]) + abs(position[1] - self.goal_position[1])

    def _reconstruct_path(self, parent_map):
        """
        Reconstruct the path from the parent map.
        
        :param parent_map: Dictionary mapping each position to its parent.
        :return: List of positions representing the path from start to goal.
        """
        path = []
        current_position = self.goal_position
        while current_position in parent_map:
            path.append(current_position)
            current_position = parent_map[current_position]
        path.reverse()
        return path

    def _is_path_blocked(self, start_position, maze):
        if maze[start_position[1]][start_position[0]] == 1:
            print("Error: Starting position is blocked.")
            return True

        if maze[self.goal_position[1]][self.goal_position[0]] == 1:
            print("Error: Goal position is blocked.")
            return True
        
        return False
    
    def validate_connectivity(self, maze):
        rows, cols = len(maze), len(maze[0])
        queue = Queue()
        queue.put(self.start_position)
        visited = set()
        visited.add(self.start_position)

        while not queue.empty():
            x, y = queue.get()
            for neighbor in self._get_neighbors((x, y), maze, rows, cols):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.put(neighbor)

        if self.goal_position not in visited:
            print("Error: Goal is unreachable from the start position.")
            return False

        return True
