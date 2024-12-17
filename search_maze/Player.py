class Player:
    def __init__(self, start_position):
        self.position = list(start_position)

    def move(self, maze, direction):
        x, y = self.position
        if direction == "UP" and maze[y - 1][x] == 0:
            self.position[1] -= 1
        elif direction == "DOWN" and maze[y + 1][x] == 0:
            self.position[1] += 1
        elif direction == "LEFT" and maze[y][x - 1] == 0:
            self.position[0] -= 1
        elif direction == "RIGHT" and maze[y][x + 1] == 0:
            self.position[0] += 1
