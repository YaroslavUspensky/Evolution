import pygame

from random import randint
from settings import *


class Cell(pygame.sprite.Sprite):
    last_move = 0

    def __init__(self, initial_x: int, initial_y: int, initial_resistance: int, initial_energy: float) -> None:
        super().__init__()
        self.image = pygame.image.load("Sprites/Cell.png")
        self.rect = self.image.get_rect()
        self.rect.x = initial_x
        self.rect.y = initial_y

        self.speed: int = 4
        self.lifetime: int = 0
        self.max_lifetime: int = 10*FPS
        self.energy: float = initial_energy

        self.resistance = initial_resistance

        self.sensitive: int = 40
        self.neighbour = [WIDTH*WIDTH + HEIGHT*HEIGHT, -1, -1]

    def change_zone(self) -> None:
        if WIDTH/4 < self.rect.x < WIDTH/2:
            if self.resistance < 20:
                self.max_lifetime = 8*FPS
        elif WIDTH/2 < self.rect.x < 3*WIDTH/4:
            if self.resistance < 50:
                self.max_lifetime = 5*FPS
        elif 3*WIDTH/4 < self.rect.x < WIDTH:
            if self.resistance < 100:
                self.max_lifetime = 2*FPS

    def mutate(self) -> None:
        if randint(0, CELL_MUTATION_PROBABILITY) == 1:
            self.resistance += 10
        # мутация уменьшения устойчивости
        # elif randint(0, MUTATION_PROBABILITY) == 2:
        #     self.resistance -= 10

    def duplicate(self):
        child = Cell(self.rect.x + 5, self.rect.y, self.resistance, self.energy//2)
        self.energy //= 2
        return child

    def move_directional(self, target_x, target_y) -> int:  # возвр. число, отвечающее за направление движения
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery

        # 0 - вверх
        # 1 - вправо
        # 2 - вниз
        # 3 - влево

        if abs(dx) > abs(dy):
            if dx > 0:
                n = 1
            else:
                n = 3
        else:
            if dy > 0:
                n = 2
            else:
                n = 0

        return n

    def move(self, n: int) -> None:

        if n >= 4:
            n = self.last_move

        if n == 0:  # вверх
            self.rect.y -= self.speed
        elif n == 1:  # вправо
            self.rect.x += self.speed
        elif n == 2:  # вниз
            self.rect.y += self.speed
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

    def locator(self) -> None:
        if self.neighbour[0] > (self.sensitive * self.sensitive):
            self.neighbour[0] = -1

    def update(self) -> None:
        self.lifetime += 1

        if self.energy < 50:
            self.locator()
            if self.neighbour[0] > 0:
                n = self.move_directional(self.neighbour[1], self.neighbour[2])
            else:
                n = randint(0, 9)
        else:
            n = randint(0, 9)
        self.move(n)

        self.mutate()
        self.change_zone()

        if self.lifetime >= self.max_lifetime or self.energy <= 0:
            self.kill()
            return
