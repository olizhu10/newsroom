import sys
import jsonl
from fragments import Fragments
import matplotlib
matplotlib.use('TkAgg')
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
    fig = plt.figure(figsize=(13,8))
    fig.add_subplot(223)
    plt.xlabel('coverage')
    plt.ylabel('density')
    for x in range(len(matrix)):
        coverages = []
        densities = []
        title = matrix[x][0].getTitle()[:20]
        for obj in matrix[x]:
            coverages.append(obj.getCoverage())
            densities.append(obj.getDensity())
        plt.scatter(coverages, densities, marker = 'o', c=COLORS[x], label=title, alpha=0.6)
    plt.legend(bbox_to_anchor=(1.05,1), loc=2, borderaxespad=0.)
    return plt

def complot(cluster):
    """Generates a dot plot for the compression for the inputted matrix"""

    matrix = create_matrix(cluster)
    fig = plt.figure(figsize=(13,8))
    fig.add_subplot(223)
    plt.xlabel('article')
    plt.ylabel('compression')
    for x in range(len(matrix)):
        compressions = []
        title = matrix[x][0].getTitle()[:20]
        for obj in matrix[x]:
            compressions.append(obj.getCompression())
        plt.scatter([x]*len(compressions), compressions, marker='o', c=COLORS[x], label=title, alpha=0.6)
    plt.legend(bbox_to_anchor=(1.05,1), loc=2, borderaxespad=0.)
    return plt

class ASData(object):
    """A class representing data for an article-summary analysis

    INSTANCE ATTRIBUTES:
        _match [bool]: whether or not the summary is a match for the article
        _data [str]: name of jsonl file with articles
        _coverage [float]: the coverage for the article-summary pair
        _density [float]: the density for the article-summary pair
        _compression [float]: the compression for the article-summary pair
        _title [str]: the title of the article
        """

    def __init__(self, article, summary, title, match, coverage = None, density = None, compression = None):
        self._match = match
        self._article = article
        self._summary = summary
        self._title = title
        if match == True:
            self._coverage = coverage
            self._density = density
            self._compression = compression

    def getMatch(self):
        return self._match

    def getTitle(self):
        return self._title

    def getCoverage(self):
        return self._coverage

    def getDensity(self):
        return self._density

    def getCompression(self):
        return self._compression

    def __repr__(self):
        if self._match == True:
            return "Coverage: "+str(self._coverage)+", Density: "+str(self._density)+", Compression: "+str(self._compression)+'\n'
        else:
            return "Not a match\n"

if __name__ == '__main__':
    colors()
