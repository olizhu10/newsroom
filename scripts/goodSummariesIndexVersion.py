import sys
import jsonl
from multiprocessing import Pool
from threading import Lock
from tqdm import tqdm
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from goodSummaries import analyzeCluster, createDictionary
import json

def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent

with jsonl.open('../clustering/final_clusters_cleaned0.9_2.jsonl') as f:
    clusters = f.read()
with jsonl.open('../dataset_files/train.jsonl.gz', gzip=True) as ds:
    articles = ds.read()
dict = createDictionary

def main():
    articleDict = {}
    pbar = tqdm(total=len(clusters), desc='Going through Clusters:')
    with jsonl.open('../clustering/cluster_pairings.jsonl') as writeFile:
        with Pool(processes=15) as pool:
            for smallDict in pool.imap(analyzeCluster, range(len(clusters))):
                writeFile.appendline(smallDict)
                pbar.update(1)

if __name__ == '__main__':
    main()
