import sys
from layout import *
from settings import *
from food import Food


class Main:
    def __init__(self):

        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Evolution")
        self.FPS = FPS
        self.clock = pygame.time.Clock()
        self.time = 0
        self.paused = False

    def run(self):

        for i in range(INITIAL_CELLS):
            Cell(randint(0, WIDTH/4), randint(0, HEIGHT), initial_resistance=0, initial_energy=100)
        for i in range(INITIAL_FOOD):
            Food()

        running = True
        while running:
            self.time += 1
            self.clock.tick(self.FPS)
            self.window.fill((255, 255, 255))

            if self.time % FOOD_RESPAWN_DELAY == 0:
                for i in range(int(INITIAL_FOOD/50)):
                    food = Food()

            eat = pygame.sprite.groupcollide(cell_sprites, food_sprites, False, True)

            for col in eat:
                for c in cell_sprites:
                    if col == c:
                        c.energy += 60

            pygame.draw.rect(self.window, (200, 186, 206), (WIDTH/4, 0, WIDTH/4, HEIGHT))
            pygame.draw.rect(self.window, (200, 156, 206), (WIDTH / 2, 0, WIDTH / 4, HEIGHT))
            pygame.draw.rect(self.window, (200, 130, 206), (3 * WIDTH / 4, 0, WIDTH / 4, HEIGHT))

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
