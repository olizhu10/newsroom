import sys
import jsonl
from ASData import ASData
from fragments import Fragments
import matplotlib.pyplot as plt

"""Creates matrix of article-summary pairs stored as ASData objects"""
def data_matrix():
    #enter name of event (string)
    event="Orlando"
    path = "../events/"+event+".jsonl"
    with jsonl.open(path, gzip = False) as train_file:
        articles = train_file.read()

    summaries = []
    for article in articles:
        summaries.append(article['summary'])

    # Compute stats on random training example:
    #article_str = sys.argv[2]
    #article_list = article_str.split()

    #lists for the indices of valid summaries for each article
    summary_lists = [[0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10]]

    '''[[0,2,3], #summaries for article 0
        [0,1,3,6,7,8], #summaries for article 1, etc
        [1,2,3,6,7],
        [0,2,3,4,7,8,9,10],
        [0,2,3,4,7,8],
        [1,3,4,5,8],
        [0,2,3,4,6,7],
        [0,2,3,4,7,8,9,10],
        [3,8],
        [0,2,3,4,7,8,9,10],
        [0,2,9,10]]'''
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

def plot(matrix):
    coverages = []
    densities = []
    for x in matrix:
        for obj in x:
            if obj.getMatch() == True:
                coverages.append(obj.getCoverage())
                densities.append(obj.getDensity())
    plt.scatter(coverages, densities, marker = 'o')
    plt.show()

if __name__ == '__main__':
    plot(data_matrix())
