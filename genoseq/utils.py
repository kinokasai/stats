import math
import matplotlib.pyplot as plt


def grid_axes(nb_subplots):
    size = math.ceil(math.sqrt(nb_subplots))
    axes = []
    for i in range(nb_subplots):
        y = i // size
        x = i % size
        axes.append(plt.subplot2grid((size, size), (y, x)))
    return axes
