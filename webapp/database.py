import sqlite3

DATABASE_NAME = 'databases/databaseRefined_0.9.db'

def get_articles(cluster_id):
    db = sqlite3.connect(DATABASE_NAME)
    c = db.cursor()
    q = "SELECT * FROM articles WHERE cluster=?"
    t = (cluster_id,)
    c.execute(q,t)
    articles = c.fetchall()
    return articles

def remove_cluster(cluster_id):
    db = sqlite3.connect(DATABASE_NAME)
    c = db.cursor()
    q = "REMOVE FROM articles WHERE cluster=?"
    t = (cluster_id,)
    c.execute(q,t)
    return
