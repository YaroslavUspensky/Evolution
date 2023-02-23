import sys
from layout import *


class Main:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Evolution")
        self.FPS = FPS
        self.clock = pygame.time.Clock()
        self.paused = False

    def run(self):
        for i in range(5):
            cell = Cell(randint(0, WIDTH//4), randint(0, HEIGHT), 0)
            all_sprites.add(cell)
            cell_sprites.add(cell)

        running = True
        while running:
            self.clock.tick(self.FPS)
            self.window.fill((255, 255, 255))
            pygame.draw.rect(self.window, (255, 206, 206), (WIDTH/4, 0, WIDTH/4, HEIGHT))
            pygame.draw.rect(self.window, (238, 176, 176), (WIDTH / 2, 0, WIDTH / 4, HEIGHT))
            pygame.draw.rect(self.window, (255, 146, 146), (3 * WIDTH / 4, 0, WIDTH / 4, HEIGHT))
            all_sprites.update()
            all_sprites.draw(self.window)

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # конечная численность клеток
                    # print(len(cell_sprites))
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.pause()

    def pause(self):
        self.paused = True
        while self.paused:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_SPACE:
                        self.paused = False
        self.clock.tick(FPS)


main = Main()
main.run()
