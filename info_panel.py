import pygame
from cell import Cell
from settings import WIDTH, HEIGHT

pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Arial.ttf", 16)


class InfoPanel(pygame.sprite.Sprite):
    def __init__(self, window, cell: Cell):
        super().__init__()
        self.window = window
        self.image = pygame.Surface((80, 60))
        self.image.fill((90, 90, 90))
        self.rect = window.get_rect()

        if cell.rect.centerx > WIDTH - 80:
            self.rect.x = cell.rect.centerx - 80

        else:
            self.rect.x = cell.rect.centerx

        if cell.rect.centery > HEIGHT - 60:
            self.rect.y = cell.rect.centery - 60
        else:
            self.rect.y = cell.rect.centery

        self.text = f"Lifetime: {cell.lifetime}\n" \
                    f"Energy: {round(cell.energy, 2)}\n" \
                    f"Resistance: {cell.resistance}\n" \
                    f"Position:\n{cell.rect.center}"

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


class InputBox(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, text, text_input=""):
        super().__init__()
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (150, 150, 150)
        self.text = text
        self.text_input = text_input
        self.text_surface = font.render(self.text, True, (0, 0, 0))
        self.text_inp_surface = font.render(self.text_input, True, (0, 0, 0))
        self.active = False

    def handle_event(self, event, parameter):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False

            if self.active:
                self.color = (0, 90, 40)
            else:
                self.color = (150, 150, 150)

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    parameter = int(self.text_input)
                    print(self.text_input)
                    self.text_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.text_input = self.text_input[:-1]
                else:
                    self.text_input += event.unicode
                self.text_inp_surface = font.render(self.text_input, True, (0, 0, 0))

        return parameter

    def update(self) -> None:
        self.text_surface = font.render(self.text, True, (0, 0, 0))

    def draw(self, window: pygame.Surface):
        window.blit(self.text_surface, (self.rect.x - 150, self.rect.y))
        window.blit(self.text_inp_surface, (self.rect.x, self.rect.y))

        pygame.draw.rect(window, self.rect, self.rect, 2)




