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


def average(window, identifier):
    return

def cluster():
    with jsonl.open('../clustering/clusters.jsonl') as file:
        windows = jsonl.read(file)
    identifier = get_identifier(True)

    x = 2
    w1 = windows[x-2]
    w2 = windows[x-1]
    w3 = windows[x]
    while x < len(windows):
        matrix = average(w1, w2, w3, identifier)
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

def group(clusters):
    fileName = '../clustering/final_clusters.jsonl'
    with jsonl.open(fileName) as file:
        for key in clusters:
            if key == '-1':
                for cluster in clusters[key]:
                    file.appendline(cluster)
            else:
                file.appendline(merge(clusters[key]))

def merge(clusters):
    merged_cluster = []
    for cluster in clusters:
        for article in cluster:
            if article not in merged_cluster:
                merged_cluster.append(article)

    return merged_cluster

def read_clusters():
    pp = pprint.PrettyPrinter()
    fileName = '../clustering/final_clusters.jsonl'
    with jsonl.open(fileName) as file:
        clusters = jsonl.read(file)
    count = 0
    for cluster in clusters:
        print('cluster '+str(count)+':')
        pp.pprint(cluster)

if __name__ == '__main__':
    test()
