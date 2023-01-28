from random import randint
from typing import List
# import pygame


class Grid:

    def __init__(self):
        self.WIDTH = 100
        self.HEIGHT = 50
        self.grid = [[] * self.WIDTH for i in range(self.HEIGHT)]
        self.FOOD_COLOR = (0, 150, 0)

    def fill_with_food(self):
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                if randint(0, 5) == 0:
                    self.grid[y].append(1)
                else:
                    self.grid[y].append(0)

    def add_cell(self, position: tuple):
        cell = Cell((position[0], position[1]))
        self.grid[position[0]][position[1]] = 2
        return cell


class Cell:
    def __init__(self, initial_position: tuple):
        self.CELL_COLOR = (72, 61, 139)
        self.position = initial_position
        self.food_nearby = []

    def find_food(self, grid: List[List]):
        for y_local in range(self.position[0]-2, self.position[0]+3):
            for x_local in range(self.position[1]-2, self.position[1]+3):
                try:
                    if grid[y_local][x_local] == 1:
                        self.food_nearby.append((y_local, x_local))
                except IndexError as e:
                    return y_local, x_local, e
