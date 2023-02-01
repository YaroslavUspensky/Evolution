import sys
import pygame
from layout import *


class Main:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((800, 400))
        pygame.display.set_caption("Evolution")
        self.FPS = 10
        self.clock = pygame.time.Clock()

    def run(self):

        grid = Grid()
        # grid[строка][столбец] !!!
        grid.fill_with_food()
        # у add_cell сначала строка, затем столбец !!!
        cell = grid.add_cell((25, 65))
        cell2 = grid.add_cell((25, 35))
        # cell.find_food()

        while True:
            self.clock.tick(self.FPS)
            self.window.fill((255, 255, 255))

            for c in grid.cells:
                if c.alive is False:
                    grid.grid[c.position[0]][c.position[1]] = 0
                    del c

            for y in range(grid.HEIGHT):
                for x in range(grid.WIDTH):
                    if grid.grid[y][x] == 1:
                        # у draw сначала столбец потом строка !!!
                        pygame.draw.rect(self.window, grid.FOOD_COLOR, (8*x + 2, 8*y + 2, 4, 4))
                    elif grid.grid[y][x] == 2:
                        pygame.draw.rect(self.window, grid.CELL_COLOR, (8*x, 8*y, 8, 8))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == DEATH:

                    cell.alive = False


main = Main()
main.run()
