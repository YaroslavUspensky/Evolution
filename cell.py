import pygame

from random import randint
from settings import *


all_sprites = pygame.sprite.Group()
cell_sprites = pygame.sprite.Group()
food_sprites = pygame.sprite.Group()
table_sprites = pygame.sprite.Group()


class Cell(pygame.sprite.Sprite):
    last_move = 0

    def __init__(self, initial_x, initial_y, initial_resistance, initial_energy):
        super().__init__()
        self.image = pygame.image.load("Cell.png")
        self.rect = self.image.get_rect()
        self.rect.x = initial_x
        self.rect.y = initial_y
        self.speed = 4
        self.lifetime = 0
        self.max_lifetime = 10*FPS
        self.energy = initial_energy

        self.resistance = initial_resistance
        self.concentration = 0

        self.sensitive = 40
        self.neighbour = [WIDTH*WIDTH + HEIGHT*HEIGHT, -1, -1]

        all_sprites.add(self)
        cell_sprites.add(self)

    def change_zone(self):

        if 0 < self.rect.x < WIDTH/4:
            self.concentration = 0
        elif WIDTH/4 < self.rect.x < WIDTH/2:
            self.concentration = 50
        elif WIDTH/2 < self.rect.x < 3*WIDTH/4:
            self.concentration = 100
        elif 3*WIDTH/4 < self.rect.x < WIDTH:
            self.concentration = 200

    def mutate(self):
        if randint(0, MUTATION_PROBABILITY) == 1:
            self.resistance += 10
        # мутация уменьшения устойчивости
        # elif randint(0, MUTATION_PROBABILITY) == 2:
        #     self.resistance -= 10

    def duplicate(self):
        if self.energy > 60:
            child = Cell(self.rect.x + 5, self.rect.y, self.resistance, self.energy/2)
            self.energy /= 2
            all_sprites.add(child)
            cell_sprites.add(child)

    # ничего не работает
    # def nearest_neighbours(self) -> None:
    #
    #     for f in food_sprites:
    #         dx = f.rect.centerx - self.rect.centerx
    #         dy = f.rect.centery - self.rect.centery
    #         dist = dx**2 + dy**2
    #         if dist < (self.sensitive**2):
    #             target_x = f.rect.x
    #             target_y = f.rect.y
    #             self.neighbour[0] = dist
    #             self.neighbour[1] = target_x
    #             self.neighbour[2] = target_y
    #         else:
    #             self.neighbour[0] = -1

    def move_directional(self, target_x, target_y) -> int:  # возвр. число, отвечающее за направление движения
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        if abs(dx) > abs(dy):
            if dx < 0:
                n = 3
            else:
                n = 0
        else:
            if dy < 0:
                n = 1
            else:
                n = 4

        return n

    # мир зациклен только вертикально
    def move(self, n):

        if n > 4:
            n = self.last_move

        if n == 0:  # вправо
            self.rect.x += self.speed
        elif n == 1:  # вниз
            self.rect.y += self.speed
        elif n == 2:  # вверх
            self.rect.y -= self.speed
        elif n == 3:  # влево
            self.rect.x -= self.speed
        self.last_move = n

        if self.rect.right > WIDTH:
            self.rect.x -= self.speed
        if self.rect.left < 0:
            self.rect.x += self.speed
        if self.rect.top < 0:
            self.rect.y += self.speed
        if self.rect.bottom > HEIGHT:
            self.rect.y -= self.speed

        self.energy -= 0.1

    def locator(self):
        if self.neighbour[0] > (self.sensitive * self.sensitive):
            self.neighbour[0] = -1

    def update(self):
        self.locator()
        if self.neighbour[0] > 0:
            n = self.move_directional(self.neighbour[1], self.neighbour[2])
        else:
            n = randint(0, 12)

        self.move(n)

        self.lifetime += 1
        self.mutate()
        self.change_zone()

        if self.resistance < self.concentration:
            self.max_lifetime = 10*FPS - self.concentration

        if self.lifetime >= self.max_lifetime or self.energy <= 0:
            self.kill()
            return

        if self.lifetime % (4*FPS) == 0:
            self.duplicate()
