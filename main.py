from cell import *
from settings import *
from food import Food
from info_panel import InfoPanel
from statistics import Statistics
import pandas


all_sprites = pygame.sprite.Group()
cell_sprites = pygame.sprite.Group()
food_sprites = pygame.sprite.Group()
table_sprites = pygame.sprite.Group()


class Main:
    def __init__(self):

        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Evolution")
        self.FPS = FPS
        self.clock = pygame.time.Clock()
        self.time = 0
        self.running = True
        self.era = 0

        self.stat = Statistics
        self.resistance_stats = [["resistance"]]
        self.statistics_dataframe = pandas.DataFrame(columns=["time, tick", "N cells", "mean resistance", "last zone cells"])

    def run(self, time_limit):
        # time_limit - на каком кадре заканчивать симуляцию

        for i in range(INITIAL_CELLS):
            c = Cell(randint(0, WIDTH/4), randint(0, HEIGHT), initial_resistance=0, initial_energy=100)
            all_sprites.add(c)
            cell_sprites.add(c)
        for i in range(INITIAL_FOOD):
            f = Food()
            all_sprites.add(f)
            food_sprites.add(f)

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

            # if self.time % CELL_DUPLICATION_PERIOD == 0:
            self.duplication()

            if self.time % FOOD_RESPAWN_DELAY == 0:
                for i in range(FOOD_RESPAWN):
                    f = Food()
                    all_sprites.add(f)
                    food_sprites.add(f)

            # статистика
            if self.time % ERA_PERIOD == 0:
                self.era += 1
                last_zone_cells = []
                for c in cell_sprites:
                    if c.rect.centerx > 3*WIDTH/4:
                        last_zone_cells.append(c)
                self.stat.collect_statistics(cell_sprites, last_zone_cells, self.resistance_stats, self.statistics_dataframe, self.era)

            # Обработка коллизий с едой
            eat = pygame.sprite.groupcollide(cell_sprites, food_sprites, False, True)
            for col in eat:
                for c in cell_sprites:
                    if col == c:
                        c.energy += 60

            # зоны антибиотика
            pygame.draw.rect(self.window, (200, 186, 206), (WIDTH/4, 0, WIDTH/4, HEIGHT))
            pygame.draw.rect(self.window, (200, 156, 206), (WIDTH / 2, 0, WIDTH / 4, HEIGHT))
            pygame.draw.rect(self.window, (200, 130, 206), (3 * WIDTH / 4, 0, WIDTH / 4, HEIGHT))

            # обновление, прорисовка
            all_sprites.update()
            all_sprites.draw(self.window)
            pygame.display.flip()

            if time_limit is not None:
                if self.time >= time_limit:
                    self.running = False

            if len(cell_sprites) == 0:
                self.running = False

        self.ending()

    def pause(self):
        self.running = False
        while not self.running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.ending()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_SPACE:
                        self.running = True

                if e.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for c in cell_sprites:
                        if c.rect.collidepoint(pos):
                            info_p = InfoPanel(self.window, c)
                            all_sprites.add(info_p)
                            table_sprites.add(info_p)
                            for t in table_sprites:
                                t.visualize_text()

            for t in table_sprites:
                t.kill()
            pygame.display.update()
        self.clock.tick(FPS)

    def ending(self):
        # чтобы выводились все графики сразу, у каждого должно быть interactive = True

        self.stat.plot_line("Number of cells", self.statistics_dataframe["time, tick"],
                            self.statistics_dataframe["N cells"], interactive=False)
        self.stat.plot_line("Resistance", self.statistics_dataframe["time, tick"],
                            self.statistics_dataframe["mean resistance"], interactive=False)
        self.stat.plot_line("Last zone cells", self.statistics_dataframe["time, tick"],
                            self.statistics_dataframe["last zone cells"], interactive=False)
        print(f"{self.time // FPS} c")
        pygame.quit()

    @staticmethod
    def duplication():
        for c in cell_sprites:
            if c.energy > 100:
                child = c.duplicate()
                all_sprites.add(child)
                cell_sprites.add(child)

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
# 6000 кадров - 5 минут
main.run(12000)
