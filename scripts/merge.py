import jsonl
import pprint
import sklearn
import numpy as np
import sys
from enum import Enum
from tfidf_calc import tfidf, preprocess, get_identifier
from clusters import get_tfidf
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


def average(window, identifier):
    for key in window:
        matrix = get_tfidf(archives, identifier)
        matrix.sum()
        for article in window[key]:



def merge():
    with jsonl.open('../clustering/clusters.jsonl') as file:
        windows = jsonl.read(file)
    for x in range(len(windows)):
        if x >=2:
            w1 = windows[x-2]
            w2 = windows[x-1]
            w3 = windows[x]
