import jsonl
import sklearn
from enum import Enum
from tfidf_calc import tfidf, preprocess, get_identifier
from sklearn.cluster import DBSCAN
from sklearn.cluster import OPTICS
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
from scipy.sparse import *
from scipy import *
import gensim.downloader as api
from gensim.models import TfidfModel
from gensim.corpora import Dictionary

def window(start, end):
    """
    Returns set of article archives within specified start and end time.

    start and end must be integers of format YYYYMMDDHHMMSS
    """

    path = '../dataset_files/train.jsonl.gz'
    with jsonl.open(path, gzip=True) as file:
        data = file.read()
    dataset = []
    for article in data:
        time = article['date']
        if time >= str(start) and time <= str(end):
            dataset.append(article['archive'])
        if time > str(end):
            break

    return dataset

def update_time(original, add):
    """
    original: string representing the original time of format YYYYMMDDHHMMSS
    add: positive int, amount of days to add
    """

    og_year = int(original[:4])
    og_month = int(original[4:6])
    og_day = int(original[6:8])

    new_year = og_year
    new_month = og_month
    new_day = og_day+add

    if og_month in [1,3,5,7,8,10]:
        if new_day > 31:
            new_month = og_month+1
            new_day = new_day-31
    elif og_month in [1,4,6,9,11]:
        if new_day > 30:
            new_month = og_month+1
            new_day = new_day-30
    elif og_month == 12:
        if new_day > 31:
            new_month = 1
            new_day = new_day - 31
            new_year = og_year+1
    else:
        if og_year % 4 == 0 and ((not og_year % 100 == 0) or og_year % 400 == 0):
            if new_day > 29:
                new_month = 3
                new_day = new_day-29
        else:
            if new_day > 28:
                new_month = 3
                new_day = new_day-28

    if new_month < 10:
        new_month = '0'+str(new_month)
    if new_day < 10:
        new_day = '0'+str(new_day)

    return str(new_year)+new_month+new_day+'000000'

def eps(dataset):
    ns = 4
    nbrs = NearestNeighbors(n_neighbors=ns).fit(dataset)
    distances, indices = nbrs.kneighbors(dataset)
    print(distances)
    distanceDec = sorted(distances[:,ns-1], reverse=True)
    plt.plot(indices[:,0], distanceDec)
    plt.show()


def get_tfidf(archives):
    totalWords = 1780255
    identifier = get_identifier()
    dataList = []
    rowList = []
    colList = []
    for ind, archive in enumerate(archives, start = 0):
        for pair in identifier[archive]:
            dataList.append(pair[1])
            colList.append(pair[0]-1)
            rowList.append(ind)
    return csr_matrix( (array(dataList),(array(rowList),array(colList))), shape=(len(archives), totalWords) )

def cluster(start,end):
    archives = window(start, end)
    matrix = get_tfidf(archives)
    clust = OPTICS().fit(matrix)

    plot(clust)

def plot(clust):
    space = np.arange(len(X))
    reachability = clust.reachability_[clust.ordering_]
    labels = clust.labels_[clust.ordering_]

    plt.figure(figsize=(10, 7))
    G = gridspec.GridSpec(2, 3)
    ax2 = plt.subplot(G[1, 0])

    colors = ['g.', 'r.', 'b.', 'y.', 'c.']
    for klass, color in zip(range(0, 5), colors):
        Xk = X[clust.labels_ == klass]
        ax2.plot(Xk[:, 0], Xk[:, 1], color, alpha=0.3)
    ax2.plot(X[clust.labels_ == -1, 0], X[clust.labels_ == -1, 1], 'k+', alpha=0.1)
    ax2.set_title('Automatic Clustering\nOPTICS')

    plt.tight_layout()
    plt.show()

def main():
    start = 19970101000000
    end = update_time(start,3)
    while start < 20180000000000:
        cluster(start, end)
        start = update_time(start,1)
        end = update_time(start,3)

if __name__ == '__main__':
    archives = window(20160612000000,20160614000000)
    matrix = get_tfidf(archives)
    eps(matrix)
