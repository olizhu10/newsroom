import sys
import jsonl
from multiprocessing import Pool
from threading import Lock
from tqdm import tqdm

"""
Removes articles with bad text.
"""

with jsonl.open('../clustering/final_clusters_0.9.jsonl') as f:
    clusters = f.read()
with jsonl.open('../dataset_files/train.jsonl.gz', gzip=True) as ds:
    articles = ds.read()

def createDictionary():
    dict = {}
    pbar = tqdm(total=len(articles), desc='Generating Dictionary:')
    for article in articles:
        dict[article['archive']]=article['text']
        pbar.update(1)
    return dict

def addArticle(x):
    tList = []
    content = ""
    for article in clusters[x]:
        for a in articles:
            if a['archive'] == article:
                if (content != a['text']):
                    content = a['text']
                    tList.append(article)
                break
    return tList

def main():
    with jsonl.open('../clustering/final_clusters_cleaned0.9_2.jsonl') as writeFile:
        dict = createDictionary()
        pbar = tqdm(total=len(clusters), desc='Cleaning Clusters:')
        for cluster in clusters:
            tList = []
            content = ""
            for article in cluster:
                if content != dict[article]:
                    content = dict[article]
                    tList.append(article)
            if len(tList)>1:
                writeFile.appendline(tList)
            else:
                writeFile.appendline([])
            pbar.update(1)

if __name__ == '__main__':
    main()
