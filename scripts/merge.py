import jsonl
import pprint
import sklearn
import numpy as np
import sys
from enum import Enum
from tfidf_calc import get_identifier
from clusters import get_tfidf
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
from scipy.sparse import *
from scipy import *
import gensim.downloader as api
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from tqdm import tqdm


def average(window1, window2, window3, identifier):
    totalWords = 1780255
    dataList = []
    rowList = []
    colList = []
    average_single_window(window1, identifier, rowList, colList, dataList, 0)
    average_single_window(window2, identifier, rowList, colList, dataList, len(window1))
    average_single_window(window3, identifier, rowList, colList, dataList, len(window1)+len(window2))

    return csr_matrix( (array(dataList),(array(rowList),array(colList))), shape=((len(window1)+len(window2)+len(window3)), totalWords) )

def average_single_window(window, identifier, rowList, colList, dataList, startRow):
    for ind, key in enumerate(window, start = startRow):
        matrix = get_tfidf(window[key], identifier)
        rows = np.zeros(len(window[key]))
        cols = range(len(window[key]))
        S = csr_matrix((np.ones(len(window[key])), (rows, cols)), shape=(1, len(window[key])))
        averageArray = (S * matrix).multiply(1./(matrix.shape[0]))
        for val, col in zip(averageArray.data, averageArray.indices):
            dataList.append(val)
            colList.append(col)
            rowList.append(ind)
    return

def trash():
    with jsonl.open('../clustering/clusters.jsonl') as file:
        windows = file.read()
    clean = []
    for window in windows:
        if not window == {}:
            clean.append(window)
    with jsonl.open('../clustering/clean_clusters.jsonl') as clean_file:
        clean_file.write(clean)


def cluster():
    with jsonl.open('../clustering/clusters.jsonl') as file:
        windows = file.read()
    print('getting identifier')
    identifier = get_identifier(True)

    x = 2
    w1 = windows[x-2]
    w2 = windows[x-1]
    w3 = windows[x]
    pbar = tqdm(total=len(windows), desc='clustering')
    while x < len(windows):
        if w1 == {}:
            w1=w2
            w2=w3
            w3=windows[x+1]
            continue

        matrix = average(w1, w2, w3, identifier)
        if matrix.shape[0] == 0:
            continue
        db = DBSCAN(eps=e, min_samples=2).fit(matrix)
        labels = db.labels_

        final_clusters = {}
        for x, label in enumerate(labels, 0):
            if x < len(w1):
                if str(label) in dict:
                    dict[str(label)].append(w1[x])
                else:
                    dict[str(label)] = w1[x]
            elif x >= len(w1) and x < len(w1)+len(w2):
                if str(label) in dict:
                    dict[str(label)].append(w2.pop(x-len(w1)))
            else:
                if str(label) in dict:
                    dict[str(label)].append(w3.pop(x-len(w1)-len(w2)))

        group(final_clusters)

        w1 = w2
        w2 = w3
        w3 = windows[x+1]

        pbar.update(1)

    pbar.close()

def group(clusters):
    fileName = '../clustering/final_sample_clusters.jsonl'
    with jsonl.open(fileName) as file:
        for key in tqdm(clusters, desc='grouping'):
            if key == '-1':
                for cluster in clusters[key]:
                    file.appendline(cluster)
            else:
                file.appendline(merge(clusters[key]))

def merge(clusters):
    merged_cluster = []
    for cluster in tqdm(clusters, desc='merging'):
        for article in cluster:
            if article not in merged_cluster:
                merged_cluster.append(article)

    return merged_cluster

def read_clusters():
    pp = pprint.PrettyPrinter()
    fileName = '../clustering/final_sample_clusters.jsonl'
    with jsonl.open(fileName) as file:
        clusters = file.read()
    count = 0
    for cluster in clusters:
        print('cluster '+str(count)+':')
        pp.pprint(cluster)

def sample_cluster():
    with jsonl.open('../clustering/sample_clusters2.jsonl') as file:
        windows = file.read()
    identifier = get_identifier(False)

    x = 2
    w1 = windows[x-2]
    w2 = windows[x-1]
    w3 = windows[x]
    pbar = tqdm(total=len(windows), desc='clustering')
    while x < len(windows):
        matrix = average(w1, w2, w3, identifier)
        if matrix.shape[0] == 0:
            continue
        db = DBSCAN(eps=0.9, min_samples=2).fit(matrix)
        labels = db.labels_

        dict = {}
        for x, label in enumerate(labels, 0):
            if x < len(w1):
                if str(label) in dict:
                    dict[str(label)].append(w1[x])
                else:
                    dict[str(label)] = [w1[x]]
            elif x >= len(w1) and x < len(w1)+len(w2):
                if str(label) in dict:
                    dict[str(label)].append(w2.pop(x-len(w1)))
            else:
                if str(label) in dict:
                    dict[str(label)].append(w3.pop(x-len(w1)-len(w2)))

        group(dict)

        w1 = w2
        w2 = w3
        w3 = windows[x+1]

        pbar.update(1)

    pbar.close()

if __name__ == '__main__':
    sample_cluster()
