from random import randint
from typing import List
import pygame


DEATH = pygame.USEREVENT + 1


class Grid:

    def __init__(self):
        self.WIDTH = 100
        self.HEIGHT = 50
        self.grid = [[] * self.WIDTH for i in range(self.HEIGHT)]
        self.FOOD_COLOR = (0, 150, 0)
        self.CELL_COLOR = (72, 61, 139)
        self.cells = []

    def fill_with_food(self):
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                if randint(0, 3) == 0:
                    self.grid[y].append(1)
                else:
                    self.grid[y].append(0)

    def add_cell(self, position: tuple):
        cell = Cell((position[0], position[1]), self.grid)
        self.grid[position[0]][position[1]] = 2
        self.cells.append(cell)
        return cell


class Cell:
    def __init__(self, initial_position: tuple, grid: List[List]):

        self.position = initial_position
        self.grid = grid
        self.alive = True
        pygame.time.set_timer(DEATH, 6000)

    def __del__(self):
        self.grid[self.position[0]][self.position[1]] = 0


