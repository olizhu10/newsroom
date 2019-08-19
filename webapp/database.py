import sqlite3

DATABASE_NAME = '../databases/databaseRefined_0.9.db'

def get_articles(cluster_id):
    db = sqlite3.connect(DATABASE_NAME)
    c = db.cursor()
    q = "SELECT * FROM articles WHERE cluster=?"
    t = (cluster_id,)
    c.execute(q,t)
    articles = c.fetchall()
    db.close()
    return articles

def remove_cluster(cluster_id):
    db = sqlite3.connect(DATABASE_NAME)
    c = db.cursor()
    print(cluster_id)
    q = "DELETE FROM articles WHERE cluster=?"
    t = (cluster_id,)
    c.execute(q,t)
    db.commit()
    db.close()
    return
