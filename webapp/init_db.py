import sqlite3
import sys
import jsonl
from multiprocessing import Pool
from threading import Lock
from tqdm import tqdm

db = sqlite3.connect('database.db')
c = db.cursor()
lock = Lock()
with jsonl.open('../clustering/final_clusters_0.9_cleaned.jsonl') as f:
    clusters = f.read()
with jsonl.open('../dataset_files/train.jsonl.gz', gzip=True) as ds:
    articles = ds.read()

def identity(x):
    return x

def addArticle(x):
    tList = []
    for article in clusters[x]:
        for a in articles:
            if a['archive'] == article:
                t = (a['text'], a['summary'], a['title'], a['archive'], x)
                tList.append(t)
                break
    return tList

def main():

    #Create table ARTICLES
    q = ("CREATE TABLE articles (text STRING, summary STRING, title STRING, archive STRING, cluster INTEGER)")
    c.execute(q)
    #Add articles to database
    pbar = tqdm(total=len(clusters), desc='Generating Database:')
    with Pool(processes=17) as pool:
        for tList in pool.imap_unordered(addArticle, range(len(clusters))):
            q = "INSERT INTO articles (text, summary, title, archive, cluster) VALUES (?,?,?,?,?)"
            for t in tList:
                c.execute(q, t)
                db.commit()
            pbar.update(1)


if __name__ == '__main__':
    main()
