import sys
import pygame
from layout import *


class Main:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((800, 400))
        pygame.display.set_caption("Evolution")
        self.FPS = 2
        self.clock = pygame.time.Clock()

    def run(self):

        grid = Field()
        # grid[строка][столбец] !!!
        grid.fill_with_food()
        # у add_cell сначала строка, затем столбец !!!
        cell = Cell((25, 65), grid.grid)
        grid.add_cell(cell)

        while True:
            self.clock.tick(self.FPS)
            self.window.fill((255, 255, 255))
            for c in grid.cells:
                if c.alive is False:
                    del c
                else:
                    c.live()

            for y in range(grid.GRID_HEIGHT):
                for x in range(grid.GRID_WIDTH):
                    if grid.grid[y][x] == 1:
                        # у draw сначала столбец потом строка !!!
                        pygame.draw.rect(self.window, grid.FOOD_COLOR, (8 * x, 8 * y, 8, 8))
                    elif grid.grid[y][x] == 2:
                        self.window.blit(cell.surf, cell.position)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()


main = Main()
main.run()
