class AIMetrics:
    def __init__(self, algorithm_name, path, steps, nodes_explored, path_length, execution_time, cpu_usage, memory_usage):
        self.algorithm_name = algorithm_name
        self.path = path
        self.steps = steps
        self.nodes_explored = nodes_explored
        self.path_length = path_length
        self.execution_time = execution_time
        self.cpu_usage = cpu_usage
        self.memory_usage = memory_usage

    def __str__(self):
        """String representation for easy debugging and reporting."""
        return (f"AIMetrics(\n"
                f"  Algorithm: {self.algorithm_name}\n"
                f"  Path: {self.path}\n"
                f"  Steps: {self.steps}\n"
                f"  Nodes Explored: {self.nodes_explored}\n"
                f"  Path Length: {self.path_length}\n"
                f"  Execution Time: {self.execution_time:.4f} seconds\n"
                f"  CPU Usage: {self.cpu_usage:.2f}%\n"
                f"  Memory Usage: {self.memory_usage:.2f} MB\n)")
