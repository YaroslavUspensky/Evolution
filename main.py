import sys

import pygame
from random import randint


WIDTH = 800
HEIGHT = 400
GRID_WIDTH = 100
GRID_HEIGHT = 50
AMOUNT_OF_FOOD = 5
FPS = 10

all_sprites = pygame.sprite.Group()
cell_sprites = pygame.sprite.Group()


class Cell(pygame.sprite.Sprite):
    last_move = 0

    def __init__(self, initial_x, initial_y):
        super().__init__()
        self.image = pygame.image.load("Cell.png")
        self.rect = self.image.get_rect()
        self.rect.x = initial_x
        self.rect.y = initial_y
        self.lifetime = 0
        self.max_lifetime = 10*FPS

    def update(self):
        self.lifetime += 1
        if self.lifetime >= self.max_lifetime:
            self.kill()

        if self.lifetime == 30:
            self.division()

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

    def division(self):
        child = Cell(self.rect.x + 5, self.rect.y)
        all_sprites.add(child)
        cell_sprites.add(child)


class Main:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Evolution")
        self.FPS = FPS
        self.clock = pygame.time.Clock()

    def run(self):
        for i in range(5):
            cell = Cell(randint(0, 800), randint(0, 400))
            all_sprites.add(cell)
            cell_sprites.add(cell)

        while True:
            self.clock.tick(self.FPS)
            self.window.fill((255, 255, 255))
            all_sprites.update()
            all_sprites.draw(self.window)

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print(len(cell_sprites))
                    pygame.quit()
                    sys.exit()


main = Main()
main.run()
