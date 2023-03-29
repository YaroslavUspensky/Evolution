import numpy
import matplotlib
from settings import ERA_PERIOD


def parameter_statistics(cells, parameter, matrix, era):
    matrix.append([])
    for c in cells:
        matrix[:][era].append(getattr(c, parameter))

    mean = numpy.mean(matrix[era][:])

    if len(cells) > 1:
        deviation = numpy.std(matrix[era][:])
    else:
        deviation = 0

    return mean, deviation


def collect_statistics(cells, matrix, matrix_stat, era):
    mean_resistance, deviation_resistance = parameter_statistics(cells, "speed", matrix, era)
    num_cells = len(cells)

    row = {"time, tick": era*ERA_PERIOD,
           "N cells": num_cells,
           "mean resistance": mean_resistance,
           "deviation resistance": deviation_resistance,
           }

    matrix_stat.loc[era] = row


def plot_line(N_figure, x, y, interactive=True):
    matplotlib.figure(N_figure)
    matplotlib.plot(x, y, "o-", alpha=0.4)
    matplotlib.interactive(interactive)
    matplotlib.show()
