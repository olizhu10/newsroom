import sys
import jsonl
from ASData import ASData
from fragments import Fragments
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

def get_colors():
    all_colors = list(mcolors.BASE_COLORS)
    all_colors.extend(mcolors.TABLEAU_COLORS)
    all_colors.extend(mcolors.CSS4_COLORS)

    bad_colors = ['w', 'whitesmoke', 'white', 'snow', 'mistyrose', 'seashell',
        'linen', 'oldlace', 'floralwhite', 'cornsilk', 'lemonchiffon', 'ivory',
        'beige', 'lightyellow', 'lightgoldenyellow', 'honeydew', 'mintcream', 'azure',
        'lightcyan', 'aliceblue', 'ghostwhite', 'lavenderbush']

    good_colors = []
    for color in all_colors:
        if not color in bad_colors:
            good_colors.append(color)
    return good_colors

COLORS = get_colors()

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

def cdplot(cluster):
    """Generates a scatter plot showing the relationship between coverage and
    density for the inputted matrix"""

    matrix = create_matrix(cluster)
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
        plt.scatter(coverages, densities, marker = 'o', c=COLORS[x], label=title, alpha=0.6)
    plt.legend()
    return plt

def complot(cluster):
    """Generates a dot plot for the compression for the inputted matrix"""

    matrix = create_matrix(cluster)
    plt.xlabel('article')
    plt.ylabel('compression')
    for x in range(len(matrix)):
        compressions = []
        title = matrix[x][0].getTitle()[:20]
        for obj in matrix[x]:
            if obj.getMatch() == True:
                compressions.append(obj.getCompression())
        plt.scatter([x]*len(compressions), compressions, marker='o', c=COLORS[x], label=title, alpha=0.6)
    plt.legend()
    return plt

if __name__ == '__main__':
    colors()
