from random import randint
from typing import List


import pygame


class Grid:

    def __init__(self):
        self.WIDTH = 100
        self.HEIGHT = 50
        self.grid = [[] * self.WIDTH for i in range(self.HEIGHT)]
        self.FOOD_COLOR = (0, 150, 0)

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
        return cell


class Cell:
    def __init__(self, initial_position: tuple, grid: List[List]):
        self.CELL_COLOR = (72, 61, 139)
        self.position = initial_position
        self.nearest_food = []
        self.grid = grid
        self.energy = 100
        # self.alive = True

    def find_food(self):
        food_nearby = []
        for y_local in range(self.position[0] - 2, self.position[0] + 3):
            for x_local in range(self.position[1] - 2, self.position[1] + 3):
                try:
                    if self.grid[y_local][x_local] == 1:
                        food_nearby.append((y_local, x_local))
                except IndexError as e:
                    return y_local, x_local, e

        distances = {}
        for food in food_nearby:
            if abs(self.position[0] - food[0]) == 2 or abs(self.position[1] - food[1]) == 2:
                distances[food] = 2
            else:
                distances[food] = 1

        for xy in distances.keys():
            if distances[xy] == min(distances.values()):
                self.nearest_food.append(xy)

    def move(self):
        if self.energy <= 0:
            return
        n = randint(0, 3)
        # Проблема: когда клетка доходит до границы и выходит за нее сверху, она перемещается вниз!

        if n == 0:
            lst = list(self.position)
            self.grid[lst[0]][lst[1]] = 0
            lst[0] = lst[0] - 1
            self.energy -= 1
            self.position = tuple(lst)
            if self.grid[self.position[0]][self.position[1]] == 1:
                self.energy += 10
            self.grid[lst[0]][lst[1]] = 2
        elif n == 1:
            lst = list(self.position)
            self.grid[lst[0]][lst[1]] = 0
            lst[0] = lst[0] + 1
            self.energy -= 1
            self.position = tuple(lst)
            if self.grid[self.position[0]][self.position[1]] == 1:
                self.energy += 10
            self.grid[lst[0]][lst[1]] = 2
        elif n == 2:
            lst = list(self.position)
            self.grid[lst[0]][lst[1]] = 0
            lst[1] = lst[1] - 1
            self.energy -= 1
            self.position = tuple(lst)
            if self.grid[self.position[0]][self.position[1]] == 1:
                self.energy += 10
            self.grid[lst[0]][lst[1]] = 2
        elif n == 3:
            lst = list(self.position)
            self.grid[lst[0]][lst[1]] = 0
            lst[1] = lst[1] + 1
            self.energy -= 1
            self.position = tuple(lst)
            if self.grid[self.position[0]][self.position[1]] == 1:
                self.energy += 10
            self.grid[lst[0]][lst[1]] = 2

