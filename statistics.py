import numpy
import matplotlib.pyplot
from settings import ERA_PERIOD


class Statistics:

    @staticmethod
    def collect_statistics(cells, last_zone, matrix, matrix_stat, era):
        matrix.append([])
        for c in cells:
            matrix[:][era].append(getattr(c, "resistance"))

        mean_resistance = numpy.mean(matrix[era][:])

        num_cells = len(cells)

        row = {"time, tick": era*ERA_PERIOD,
               "N cells": num_cells,
               "mean resistance": mean_resistance,
               "last zone cells": len(last_zone)
               }

        matrix_stat.loc[era] = row

    @staticmethod
    def plot_line(title: str, x, y, interactive=True):
        matplotlib.pyplot.figure(title)
        matplotlib.pyplot.plot(x, y, "-", alpha=0.4)
        matplotlib.interactive(interactive)
        matplotlib.pyplot.show()
