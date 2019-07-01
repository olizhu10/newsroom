import sqlite3
import sys
import jsonl

db = sqlite3.connect('database.db')
c = db.cursor()

#Create table ARTICLES
q = ("CREATE TABLE articles (text STRING, summary STRING, title STRING, archive STRING, cluster INTEGER)")
c.execute(q)

#Add articles to database
with jsonl.open('../clustering/final_clusters.jsonl') as f:
    clusters = f.read()
with jsonl.open('../dataset_files/train.jsonl.gz', gzip=True) as ds:
    articles = ds.read()
for x in range(len(clusters)):
    print(x)
    for article in clusters[x]:
        for a in articles:
            if a['archive'] == article:
                q = "INSERT INTO articles (text, summary, title, archive, cluster) VALUES (?,?,?,?,?)"
                t = (a['text'], a['summary'], a['title'], a['archive'], x)
                c.execute(q, t)
                break
