import numpy
import matplotlib.pyplot
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
    mean_resistance, deviation_resistance = parameter_statistics(cells, "resistance", matrix, era)
    num_cells = len(cells)

    row = {"time, tick": era*ERA_PERIOD,
           "N cells": num_cells,
           "mean resistance": mean_resistance,
           "deviation resistance": deviation_resistance,
           }

    matrix_stat.loc[era] = row


def plot_line(n_figure, x, y, interactive=True):
    matplotlib.pyplot.figure(n_figure)
    matplotlib.pyplot.plot(x, y, "o-", alpha=0.4)
    matplotlib.interactive(interactive)
    matplotlib.pyplot.show()


def boxplot(n_figure, matrix, timeline, interactive):
    matplotlib.pyplot.figure(n_figure)
    matplotlib.pyplot.boxplot(matrix[1:])
    matplotlib.pyplot.interactive(interactive)
    matplotlib.pyplot.show()
