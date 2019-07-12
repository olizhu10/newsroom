import sys
import jsonl
from multiprocessing import Pool
from threading import Lock
from tqdm import tqdm

with jsonl.open('../clustering/final_clusters_0.9.jsonl') as f:
    clusters = f.read()
with jsonl.open('../dataset_files/train.jsonl.gz', gzip=True) as ds:
    articles = ds.read()

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
    with jsonl.open('../clustering/final_clusters_0.9_cleaned.jsonl') as writeFile:
        pbar = tqdm(total=len(clusters), desc='Cleaning Clusters:')
        with Pool(processes=17) as pool:
            for tList in pool.imap_unordered(addArticle, range(len(clusters))):
                if len(tList)>1:
                    writeFile.appendline(tList)
                else:
                    writeFile.appendline([])
                pbar.update(1)

if __name__ == '__main__':
    main()
