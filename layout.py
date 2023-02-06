from random import randint
from typing import List
import pygame

DIVISION = pygame.USEREVENT + 1


class Field(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.food_img = pygame.image.load("Food.png")
        self.rect = self.food_img.get_rect()
        self.GRID_WIDTH = 100
        self.GRID_HEIGHT = 50
        self.FOOD_COLOR = (0, 140, 0)
        self.grid = [[] * self.GRID_WIDTH for i in range(self.GRID_HEIGHT)]
        self.cells = []

    def fill_with_food(self):
        for y in range(self.GRID_HEIGHT):
            for x in range(self.GRID_WIDTH):
                if randint(0, 3) == 0:
                    self.grid[y].append(1)
                else:
                    self.grid[y].append(0)

    def add_cell(self, cell):
        self.grid[cell.position[0]][cell.position[1]] = 2
        self.cells.append(cell)


class Cell(pygame.sprite.Sprite):
    def __init__(self, initial_position: tuple, grid: List[List]):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Cell.png")
        self.rect = self.image.get_rect()
        self.surf = pygame.Surface(self.rect)
        self.position = initial_position
        self.grid: List[List] = grid
        self.alive = True
        self.energy = 100

    def live(self):
        if self.energy <= 0:
            self.alive = False
            self.grid[self.position[0]][self.position[1]] = 0
        else:
            # self.move()
            # типа живет
            self.energy -= 5

    def move(self):
        n = randint(0, 3)
        if n == 0:
            temp = list(self.position)
            temp[0] -= 1
            self.grid[self.position[0]][self.position[1]] = 0
            self.position = tuple(temp)
            del temp
            self.grid[self.position[0]][self.position[1]] = 2
        elif n == 1:
            temp = list(self.position)
            temp[0] += 1
            self.grid[self.position[0]][self.position[1]] = 0
            self.position = tuple(temp)
            del temp
            self.grid[self.position[0]][self.position[1]] = 0
        elif n == 2:
            temp = list(self.position)
            temp[1] -= 1
            self.grid[self.position[0]][self.position[1]] = 0
            self.position = tuple(temp)
            del temp
            self.grid[self.position[0]][self.position[1]] = 0
        else:
            temp = list(self.position)
            temp[1] += 1
            self.grid[self.position[0]][self.position[1]] = 0
            self.position = tuple(temp)
            del temp
            self.grid[self.position[0]][self.position[1]] = 0

    def divide(self, surface: Field):
        self.grid[self.position[0]][self.position[1]] = 0
        if randint(0, 1) == 1:
            daughter_cell1 = Cell((self.position[0], self.position[1] + 1), self.grid)
            daughter_cell2 = Cell((self.position[0], self.position[1] - 1), self.grid)
        else:
            daughter_cell1 = Cell((self.position[0] + 1, self.position[1]), self.grid)
            daughter_cell2 = Cell((self.position[0] - 1, self.position[1]), self.grid)
        surface.add_cell(daughter_cell1)
        surface.add_cell(daughter_cell2)



