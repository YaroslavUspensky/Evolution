import sys
from cell import *
from random import randint
from settings import *
from food import Food
from info_panel import InfoPanel
from statistics import collect_statistics, plot_line
import pandas


class Main:
    def __init__(self):

        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Evolution")
        self.FPS = FPS
        self.clock = pygame.time.Clock()
        self.time = 0
        self.running = True
        self.era = 0

    def run(self):

        for i in range(INITIAL_CELLS):
            Cell(randint(0, WIDTH/4), randint(0, HEIGHT), initial_resistance=0, initial_energy=100)
        for i in range(INITIAL_FOOD):
            Food()

        # time_line = []
        resistance_stats = [["resistance", "era period =", ERA_PERIOD]]

        statistics_dataframe = pandas.DataFrame(columns=["time, tick", "N cells", "mean resistance", "deviation resistance"])

        while self.running:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.pause()

            self.nearest_neighbours()

            self.time += 1
            self.window.fill((255, 255, 255))

            if self.time % FOOD_RESPAWN_DELAY == 0:
                for i in range(int(INITIAL_FOOD/50)):
                    Food()

            if self.time % ERA_PERIOD == 0:
                self.era += 1
                # time_line.append(self.era*ERA_PERIOD)
                collect_statistics(cell_sprites, resistance_stats, statistics_dataframe, self.era)

            eat = pygame.sprite.groupcollide(cell_sprites, food_sprites, False, True)
            for col in eat:
                for c in cell_sprites:
                    if col == c:
                        c.energy += 60

            # зоны антибиотика
            pygame.draw.rect(self.window, (200, 186, 206), (WIDTH/4, 0, WIDTH/4, HEIGHT))
            pygame.draw.rect(self.window, (200, 156, 206), (WIDTH / 2, 0, WIDTH / 4, HEIGHT))
            pygame.draw.rect(self.window, (200, 130, 206), (3 * WIDTH / 4, 0, WIDTH / 4, HEIGHT))

            all_sprites.update()
            all_sprites.draw(self.window)
            pygame.display.flip()

            if len(cell_sprites) == 0:
                self.running = False

        # статистика
        plot_line(1, statistics_dataframe["time, tick"], statistics_dataframe["N cells"], interactive=False)
        plot_line(2, statistics_dataframe["time, tick"], statistics_dataframe["mean resistance"], interactive=False)

        # statistics_dataframe.to_excel("output_simulation_stat.xlsx")

        print(f"{self.time // FPS} c")
        pygame.quit()
        sys.exit()

    def pause(self):
        self.running = False
        while not self.running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_SPACE:
                        self.running = True
                if e.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for c in cell_sprites:
                        if c.rect.collidepoint(pos):
                            InfoPanel(self.window, c)
                            for t in table_sprites:
                                t.visualize_text()

            for t in table_sprites:
                t.kill()
            pygame.display.update()
        self.clock.tick(FPS)

    @staticmethod
    def nearest_neighbours():
        for c in cell_sprites:
            min_distance = WIDTH * WIDTH + HEIGHT * HEIGHT
            if len(food_sprites) > 0:
                for f in food_sprites:
                    dx = c.rect.centerx - f.rect.centerx
                    dy = c.rect.centery - f.rect.centery
                    dist = dx * dx + dy * dy
                    if dist < min_distance:
                        min_distance = dist
                        coord_x_target = f.rect.centerx
                        coord_y_target = f.rect.centery
                c.neighbour[1] = coord_x_target
                c.neighbour[2] = coord_y_target
                c.neighbour[0] = min_distance


main = Main()
main.run()
