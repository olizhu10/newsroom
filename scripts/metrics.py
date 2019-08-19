import sys
import jsonl
from ASData import ASData
from fragments import Fragments
import matplotlib.pyplot as plt
import matplotlib.colors
import numpy as np

"""
Creates plots to view coverage, density, and compression data of article-summary
pairs in a cluster.
"""
def data_matrix(event):
    """Creates matrix of article-summary pairs stored as ASData objects"""

    #enter name of event (string)
    path = "../events/"+event+".jsonl"
    with jsonl.open(path, gzip = False) as train_file:
        articles = train_file.read()

    summaries = []
    for article in articles:
        summaries.append(article['summary'])

    #lists for the indices of valid summaries for each article
    if event == 'Mandela':
        summary_lists = [
            [0,2,8],
            [1,2],
            [0,2],
            [0,2,3,6,7],
            [0,2,4,5,6,7,8],
            [0,2,5,6,7],
            [5,6],
            [7],
            [8]
        ]

    elif event == 'Orlando':
        summary_lists = [
            [0,2,3], #summaries for article 0
            [0,1,3,6,7,8], #summaries for article 1, etc
            [1,2,3,6,7],
            [0,2,3,4,7,8,9,10],
            [0,2,3,4,7,8],
            [1,3,4,5,8],
            [0,2,3,4,6,7],
            [0,2,3,4,7,8,9,10],
            [3,8],
            [0,2,3,4,7,8,9,10],
            [0,2,9,10]
        ]

    elif event == 'bostonMarathon':
        summary_lists = [
            [0,1,2,4,5,6,7,8],
            [0,1,2,4,5,6,7,8],
            [0,1,2,3,4,5,6,7,8],
            [0,1,2,4,5,6,7,8],
            [0,1,2,4,5,6,7,8],
            [0,1,2,4,5,6,7,8],
            [0,1,2,4,5,6,7,8],
            [0,1,2,4,5,6,7,8],
            [0,1,2,4,5,6,7,8]
        ]

    elif event == 'hurricaneSandy':
        summary_lists = [
            [0,2,3,4],
            [0,1,4],
            [1,2,3],
            [3,5],
            [0,1,2,4],
            [2,4,5]
        ]

    else:
        raise InputError('You did not input a valid event.')

    matrix = []
    num = 0
    for article in articles:
        text = article['text']
        title = article['title']
        entries = []
        for index in range(len(summaries)):
            summary = summaries[index]
            if index in summary_lists[num]:
                #print('in if')
                fragments = Fragments(summary, text)
                obj = ASData(article, summary, title, True, fragments.coverage(),
                    fragments.density(), fragments.compression())
                entries.append(obj)
            else:
                #print('in else')
                obj = ASData(article, summary, title, False)
                entries.append(obj)
        matrix.append(entries)
        num += 1

    return matrix

def cdplot(matrix):
    """Generates a scatter plot showing the relationship between coverage and
    density for the inputted matrix"""

    colors = ['red','blue','pink','yellow','black','orange','purple','green','cyan',
    'magenta','grey']
    plt.title(event)
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
    plt.show()

def complot(matrix):
    """Generates a dot plot for the compression for the inputted matrix"""

    colors = ['red','blue','pink','yellow','black','orange','purple','green','cyan',
    'magenta','grey']
    plt.title(event)
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
    plt.show()

if __name__ == '__main__':
    event = input('event: ')
    complot(data_matrix())
