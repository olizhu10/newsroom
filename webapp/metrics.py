import sys
import jsonl
from ASData import ASData
from fragments import Fragments
import matplotlib.pyplot as plt
import matplotlib.colors
import numpy as np

def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)

def cdplot(matrix):
    """Generates a scatter plot showing the relationship between coverage and
    density for the inputted matrix"""

    colors = ['red','blue','pink','yellow','black','orange','purple','green','cyan',
    'magenta','grey']
    cmap=get_cmap(len(matrix))
    plt.xlabel('coverage')
    plt.ylabel('density')
    for x in range(len(matrix)):
        coverages = []
        densities = []
        title = matrix[x][0].getTitle()[:20]
        for obj in matrix[x]:
            if obj.getMatch() == True:
                coverages.append(obj.getCoverage())
                densities.append(obj.getDensity())
        plt.scatter(coverages, densities, marker = 'o', c=cmap(x), label=title, alpha=0.6)
    plt.legend()
    return plt

def complot(matrix):
    """Generates a dot plot for the compression for the inputted matrix"""

    colors = ['red','blue','pink','yellow','black','orange','purple','green','cyan',
    'magenta','grey']
    plt.xlabel('article')
    plt.ylabel('compression')
    for x in range(len(matrix)):
        compressions = []
        title = matrix[x][0].getTitle()[:20]
        for obj in matrix[x]:
            if obj.getMatch() == True:
                compressions.append(obj.getCompression())
        plt.scatter([x]*len(compressions), compressions, marker='o', c=colors[x], label=title, alpha=0.6)
    plt.legend()
    return plt
