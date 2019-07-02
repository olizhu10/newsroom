import jsonl
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
    identifier = get_identifier(True)

    ind = 2
    w2 = windows[ind-2]
    w3 = windows[ind-1]
    w2length = len(w2)
    w3length = len(w3)
    pbar = tqdm(total=len(windows), desc='clustering', initial=2)
    while ind < len(windows):
        w1 = w2
        w2 = w3
        w3 = windows[ind]
        w1length = w2length
        w2length = w3length
        w3length = len(w3)
        if(len(w1) == 0):
            ind+=1
            pbar.update(1)
            continue;
        matrix = average(w1, w2, w3, identifier)
        if matrix.shape[0] == 0:
            continue
        db = DBSCAN(eps=0.8, min_samples=2).fit(matrix)
        labels = db.labels_
        count = 0
        dict = {}
        for x, label in enumerate(labels, start = 0):
            if x+count < w1length:
                if not(str(x+count) in w1):
                    count += 1
                    continue
                if str(label) in dict:
                    dict[str(label)].append(w1[str(x+count)])
                else:
                    dict[str(label)] = [w1[str(x+count)]]
            elif x+count >= w1length and x+count <w1length + w2length:
                if not(str(x+count-w1length) in w2):
                    count += 1
                    continue
                if str(label) in dict:
                    dict[str(label)].append(w2.pop(str(x+count-w1length)))
            else:
                if not(str(x+count-w1length-w2length) in w3):
                    count += 1
                    continue
                if str(label) in dict:
                    dict[str(label)].append(w3.pop(str(x+count-w1length-w2length)))
        group(dict)
        ind += 1
        pbar.update(1)

    pbar.close()

def group(clusters):
    fileName = '../clustering/final_clusters.jsonl'
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

def sample_cluster():
    with jsonl.open('../clustering/sample_clusters.jsonl') as file:
        windows = file.read()
    identifier = get_identifier(False)

    ind = 2
    w2 = windows[ind-2]
    w3 = windows[ind-1]
    w2length = len(w2)
    w3length = len(w3)
    pbar = tqdm(total=len(windows), desc='clustering')
    print(len(windows))
    while ind < len(windows):
        w1 = w2
        w2 = w3
        w3 = windows[ind]
        w1length = w2length
        w2length = w3length
        w3length = len(w3)
        if(len(w1) == 0):
            ind+=1
            pbar.update(1)
            continue;
        matrix = average(w1, w2, w3, identifier)
        if matrix.shape[0] == 0:
            continue
        db = DBSCAN(eps=0.8, min_samples=2).fit(matrix)
        labels = db.labels_
        count = 0
        dict = {}
        for x, label in enumerate(labels, start = 0):
            if x+count < w1length:
                if not(str(x+count) in w1):
                    count += 1
                    continue
                if str(label) in dict:
                    dict[str(label)].append(w1[str(x+count)])
                else:
                    dict[str(label)] = [w1[str(x+count)]]
            elif x+count >= w1length and x+count <w1length + w2length:
                if not(str(x+count-w1length) in w2):
                    count += 1
                    continue
                if str(label) in dict:
                    dict[str(label)].append(w2.pop(str(x+count-w1length)))
            else:
                if not(str(x+count-w1length-w2length) in w3):
                    count += 1
                    continue
                if str(label) in dict:
                    dict[str(label)].append(w3.pop(str(x+count-w1length-w2length)))
        group(dict)
        ind += 1
        pbar.update(1)

    pbar.close()

def test_cluster():
    with jsonl.open('../clustering/clusters.jsonl') as file:
        windows = file.read()
    identifier = get_identifier(True)

    ind = 6907
    w2 = windows[ind-2]
    w3 = windows[ind-1]
    w2length = len(w2)
    w3length = len(w3)
    while ind < 6912:
        w1 = w2
        w2 = w3
        w3 = windows[ind]
        w1length = w2length
        w2length = w3length
        w3length = len(w3)
        if(len(w1) == 0):
            ind+=1
            pbar.update(1)
            continue;
        matrix = average(w1, w2, w3, identifier)
        if matrix.shape[0] == 0:
            continue
        db = DBSCAN(eps=0.8, min_samples=2).fit(matrix)
        labels = db.labels_
        count = 0
        dict = {}

        ind += 1

if __name__ == '__main__':
    cluster()
