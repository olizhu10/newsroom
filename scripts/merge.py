import jsonl
import sklearn
import numpy as np
import pprint
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
import CW


def average(window1, window2, window3, w1length, w2length, w3length, identifier):
    totalWords = 1780255
    dataList = []
    rowList = []
    colList = []
    average_single_window(window1, identifier, rowList, colList, dataList, 0)
    average_single_window(window2, identifier, rowList, colList, dataList, w1length)
    average_single_window(window3, identifier, rowList, colList, dataList, w1length+w2length)

    return csr_matrix( (array(dataList),(array(rowList),array(colList))), shape=((w1length+w2length+w3length), totalWords) )

def average_single_window(window, identifier, rowList, colList, dataList, startRow):
    for key in window:
        matrix = get_tfidf(window[key], identifier)
        rows = np.zeros(len(window[key]))
        cols = range(len(window[key]))
        S = csr_matrix((np.ones(len(window[key])), (rows, cols)), shape=(1, len(window[key])))
        averageArray = (S * matrix).multiply(1./(matrix.shape[0]))
        for val, col in zip(averageArray.data, averageArray.indices):
            dataList.append(val)
            colList.append(col)
            rowList.append(startRow+int(key))
    return

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
        matrix = average(w1, w2, w3, w1length, w2length, w3length, identifier)
        if matrix.shape[0] == 0:
            continue
        db = DBSCAN(eps=0.22, min_samples=2).fit(matrix)
        labels = db.labels_
        dict = {}
        for x, label in enumerate(labels, start = 0):
            if x < w1length:
                if not(str(x) in w1):
                    continue
                if str(label) in dict:
                    dict[str(label)].append(w1[str(x)])
                else:
                    dict[str(label)] = [w1[str(x)]]
            elif x >= w1length and x <w1length + w2length:
                if not(str(x-w1length) in w2):
                    continue
                if str(label) in dict and label >= 0:
                    dict[str(label)].append(w2.pop(str(x-w1length)))
            else:
                if not(str(x-w1length-w2length) in w3):
                    continue
                if str(label) in dict and label >= 0:
                    dict[str(label)].append(w3.pop(str(x-w1length-w2length)))
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

if __name__ == '__main__':
    cluster()
