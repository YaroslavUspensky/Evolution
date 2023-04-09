import pygame
from cell import Cell, table_sprites, all_sprites
from settings import WIDTH, HEIGHT

pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Arial.ttf", 16)


class InfoPanel(pygame.sprite.Sprite):
    def __init__(self, window, cell: Cell):
        super().__init__()
        self.window = window
        self.image = pygame.Surface((80, 80))
        self.image.fill((90, 90, 90))
        self.rect = window.get_rect()

        if cell.rect.centerx > WIDTH - 80:
            self.rect.x = cell.rect.centerx - 80

        else:
            self.rect.x = cell.rect.centerx

        if cell.rect.centery > HEIGHT - 80:
            self.rect.y = cell.rect.centery - 80
        else:
            self.rect.y = cell.rect.centery

        self.text = f"{cell.lifetime}\n{cell.energy}\n{cell.resistance}\n{cell.rect.center}"

        all_sprites.add(self)
        table_sprites.add(self)

    def visualize_text(self):
        self.blit_text()
        self.window.blit(self.image, (self.rect.x, self.rect.y))

    def blit_text(self):
        words = [line.split() for line in self.text.splitlines()]  # двумерный массив с текстом, разделенным '\n' и ' '
        space = font.size(' ')[0]
        max_width, max_height = self.image.get_size()
        x, y = 0, 0
        for line in words:
            for word in line:
                word_surface = font.render(word, True, (255, 255, 255))
                word_width, word_height = word_surface.get_size()
                if x + word_width > max_width:
                    x = 0
                    y += word_height
                self.image.blit(word_surface, (x, y))
                x += word_width + space
            x = 0
            y += word_height
