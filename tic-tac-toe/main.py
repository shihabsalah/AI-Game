import pygame
from constants import *
from game import Game

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = WINDOW_SIZE, WINDOW_SIZE
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game()

    while run:
        clock.tick(60)  # Limit to 60 frames per second
        run = game.handle_events()
        # game.update()
        game.render(WIN)

    pygame.quit()

if __name__ == "__main__":
    main()