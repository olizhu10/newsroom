import sqlite3
import sys
import jsonl
from multiprocessing import Pool
from threading import Lock
from tqdm import tqdm

db = sqlite3.connect('database0.9.db')
c = db.cursor()
lock = Lock()
with jsonl.open('../clustering/final_clusters_0.9_cleaned.jsonl') as f:
    clusters = f.read()
with jsonl.open('../dataset_files/train.jsonl.gz', gzip=True) as ds:
    articles = ds.read()

def createDictionary():
    dict = {}
    pbar = tqdm(total=len(clusters), desc='Generating Dictionary:')
    for clusterInd in range(len(clusters)):
        for article in clusters[clusterInd]:
            if article in dict:
                dict[article].append(clusterInd)
            else:
                dict[article] = [clusterInd]
        pbar.update(1)
    return dict

def main():
    #Create table ARTICLES
    q = ("CREATE TABLE articles (text STRING, summary STRING, title STRING, archive STRING, cluster INTEGER)")
    c.execute(q)
    #Add articles to database
    dict = createDictionary()
    pbar = tqdm(total=len(articles), desc='Parsing json:')
    for article in articles:
        q = "INSERT INTO articles (text, summary, title, archive, cluster) VALUES (?,?,?,?,?)"
        if(article in dict):
            for t in dict[article]:
                c.execute(q, (article['text'], article['summary'], article['title'], article['archive'], t))
                db.commit()
        pbar.update(1)


if __name__ == '__main__':
    main()
