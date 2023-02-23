from random import randint
import pygame

all_sprites = pygame.sprite.Group()
cell_sprites = pygame.sprite.Group()

WIDTH = 800
HEIGHT = 400
FPS = 10


class Cell(pygame.sprite.Sprite):
    last_move = 0

    def __init__(self, initial_x, initial_y, initial_resistance):
        super().__init__()
        self.image = pygame.image.load("Cell.png")
        self.rect = self.image.get_rect()
        self.rect.x = initial_x
        self.rect.y = initial_y
        self.lifetime = 0
        self.max_lifetime = 100

        self.resistance = initial_resistance
        self.concentration = 0

    def change_zone(self):
        if 0 < self.rect.x < WIDTH/4:
            self.concentration = 0
        elif WIDTH/4 < self.rect.x < WIDTH/2:
            self.concentration = 15
            self.max_lifetime = 85
        elif WIDTH/2 < self.rect.x < 3*WIDTH/4:
            self.concentration = 50
        elif 3*WIDTH/4 < self.rect.x < WIDTH:
            self.concentration = 80

    def mutate(self):
        if randint(0, 100) == 1:
            self.resistance += 10
            self.image.fill((100, 100, 100))

    def duplicate(self):
        child = Cell(self.rect.x + 5, self.rect.y, self.resistance)
        all_sprites.add(child)
        cell_sprites.add(child)

    def move(self):
        n = randint(0, 7)
        if n > 4:
            n = self.last_move

        if n == 0:
            self.rect.x += 4
        elif n == 1:
            self.rect.x -= 4
        elif n == 2:
            self.rect.y += 4
        elif n == 3:
            self.rect.y -= 4
        self.last_move = n

        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.top < 0:
            self.rect.bottom = HEIGHT
        if self.rect.bottom > HEIGHT:
            self.rect.top = 0

    def update(self):
        self.lifetime += 1
        self.mutate()
        self.change_zone()

        if self.resistance < self.concentration:
            self.max_lifetime = 100 - self.concentration

        if self.lifetime >= self.max_lifetime:
            self.kill()
            return
        if self.lifetime == 20:
            self.duplicate()

        self.move()


class Info(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        pass
