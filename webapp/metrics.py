import sys
import jsonl
from ASData import ASData
from fragments import Fragments
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

def create_matrix(cluster):
    articles = []
    summaries = []
    for article in cluster:
        articles.append(article)
        summaries.append(article[1])

    matrix = []
    num = 0
    for article in articles:
        text = article[0]
        title = article[2]
        entries = []
        for index in range(len(summaries)):
            summary = summaries[index]
            fragments = Fragments(summary, text)
            obj = ASData(article, summary, title, True, fragments.coverage(),
                fragments.density(), fragments.compression())
            entries.append(obj)
        matrix.append(entries)
        num += 1
    return matrix

def cdplot(matrix):
    """Generates a scatter plot showing the relationship between coverage and
    density for the inputted matrix"""

    colors = list(mcolors.BASE_COLORS)
    colors.extend(mcolors.TABLEAU_COLORS)
    colors.extend(mcolors.CSS4_COLORS)

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
        plt.scatter(coverages, densities, marker = 'o', c=colors[x], label=title, alpha=0.6)
    plt.legend()
    return plt

def complot(matrix):
    """Generates a dot plot for the compression for the inputted matrix"""

    colors = list(mcolors.BASE_COLORS)
    colors.extend(mcolors.TABLEAU_COLORS)
    colors.extend(mcolors.CSS4_COLORS)

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
