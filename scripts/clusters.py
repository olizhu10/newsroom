import jsonl
import pprint
import sklearn
import numpy as np
import sys
from enum import Enum
from tfidf_calc import tfidf, preprocess, get_identifier
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
from scipy.sparse import *
from scipy import *

def window(data, start, end):
    """
    Returns set of article archives within specified start and end time.

    start and end must be integers of format YYYYMMDDHHMMSS
    """

    dataset = []
    for article in data:
        time = article['date']
        if time >= str(start) and time <= str(end):
            dataset.append(article['archive'])

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

    return str(new_year)+str(new_month)+str(new_day)+'000000'

def eps(dataset):
    ns = 4
    nbrs = NearestNeighbors(n_neighbors=ns).fit(dataset)
    distances, indices = nbrs.kneighbors(dataset)
    print(distances)
    distanceDec = sorted(distances[:,ns-1], reverse=True)
    plt.plot(indices[:,0], distanceDec)
    plt.show()


def get_tfidf(archives, identifier):
    totalWords = 1780255
    dataList = []
    rowList = []
    colList = []
    for ind, archive in enumerate(archives, start = 0):
        for pair in identifier[archive]:
            dataList.append(pair[1])
            colList.append(pair[0])
            rowList.append(ind)
    return csr_matrix( (array(dataList),(array(rowList),array(colList))), shape=(len(archives), totalWords) )

def cluster(matrix, e):
    db = DBSCAN(eps=e, min_samples=4).fit(matrix)

    return db

def plot(db, matrix):
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)

    unique_labels = set(labels)
    colors = [plt.cm.Spectral(each)
              for each in np.linspace(0, 1, len(unique_labels))]
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = [0, 0, 0, 1]

        class_member_mask = (labels == k)

        xy = matrix[class_member_mask & core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=14)

        xy = matrix[class_member_mask & ~core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=6)

    plt.title('Estimated number of clusters: %d' % n_clusters_)

def group(labels, archives):
    fileName = '../clustering/sample_clusters2.jsonl'
    dict = {}
    with jsonl.open(fileName) as file:
        for x in range(len(labels)):
            if str(labels[x]) != '-1':
                if str(labels[x]) in dict:
                    dict[str(labels[x])].append(archives[x])
                else:
                    dict[str(labels[x])] = [archives[x]]
        file.appendline(dict)

def print_clusters():
    fileName = '../clustering/sample_clusters2.jsonl'
    pp = pprint.PrettyPrinter()
    dict = jsonl.read(fileName)
    for window in dict:
        for key in window:
            print('cluster '+key+':')
            pp.pprint(window[key])

def cluster_sampling():
    start = '20160610000000'
    end = update_time(start, 3)
    path = '../dataset_files/train.jsonl.gz'
    print('opening file')
    with jsonl.open(path, gzip=True) as file:
        data = file.read()
    print('getting identifier')
    identifier = get_identifier(False)
    print('starting clustering')
    while start < '20160615000000':
        archives = window(data, start, end)
        matrix = get_tfidf(archives,identifier)
        if matrix.shape[0] == 0:
            group([],[])
            start = update_time(start, 1)
            end = update_time(start, 3)
            count += 1
            continue
        db = cluster(matrix, 0.93)
        group(db.labels_, archives)
        start = update_time(start, 1)
        end = update_time(start, 3)

def main():
    start = '19980101000000'
    end = update_time(start, 3)
    path = '../dataset_files/train.jsonl.gz'
    print('opening file')
    with jsonl.open(path, gzip=True) as file:
        data = file.read()
    print('getting identifier')
    identifier = get_identifier(True)
    print('starting clustering')
    count = 0
    while start < '20180000000000':
        archives = window(data, start, end)
        matrix = get_tfidf(archives,identifier)
        if matrix.shape[0] == 0:
            group([],[])
            start = update_time(start, 1)
            end = update_time(start, 3)
            count += 1
            continue
        db = cluster(matrix, 0.93)
        group(db.labels_, archives)
        start = update_time(start, 1)
        end = update_time(start, 3)
        count += 1
        print(count)

if __name__ == '__main__':
    print_clusters()
