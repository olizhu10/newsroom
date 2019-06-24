import sys
import jsonl
from ASData import ASData
from fragments import Fragments
import matplotlib.pyplot as plt

"""Creates matrix of article-summary pairs stored as ASData objects"""
def data_matrix(event):
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

    else:
        raise InputError('You did not input a valid event.')

    matrix = []
    num = 0
    for article in articles:
        text = article['text']
        entries = []
        for index in range(len(summaries)):
            summary = summaries[index]
            if index in summary_lists[num]:
                #print('in if')
                fragments = Fragments(summary, text)
                obj = ASData(article, summary, True, fragments.coverage(), fragments.density(), fragments.compression())
                entries.append(obj)
            else:
                #print('in else')
                obj = ASData(article, summary, False)
                entries.append(obj)
        matrix.append(entries)
        num += 1

    return matrix

"""Generates a scatter plot for the inputted matrix"""
def plot(matrix, event):
    coverages = []
    densities = []
    for x in matrix:
        for obj in x:
            if obj.getMatch() == True:
                coverages.append(obj.getCoverage())
                densities.append(obj.getDensity())
    plt.title(event)
    plt.xlabel('coverage')
    plt.ylabel('density')
    plt.scatter(coverages, densities, marker = 'o')
    plt.savefig('../events/data/'+event+'.png')
    plt.show()

if __name__ == '__main__':
    event = input('event: ')
    plot(data_matrix(event), event)
