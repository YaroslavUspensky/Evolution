import pygame
from settings import WIDTH, HEIGHT
from random import uniform


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Sprites/Food.png")
        self.rect = self.image.get_rect()
        self.rect.center = (uniform(0, WIDTH), uniform(0, HEIGHT))
