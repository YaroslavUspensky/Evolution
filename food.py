import pygame
from cell import all_sprites, food_sprites
from settings import WIDTH, HEIGHT
from random import uniform


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Food.png")
        self.rect = self.image.get_rect()
        self.rect.center = (uniform(0, WIDTH), uniform(0, HEIGHT))
        all_sprites.add(self)
        food_sprites.add(self)
