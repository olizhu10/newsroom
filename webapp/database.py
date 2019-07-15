import sqlite3

DATABASE_NAME = 'databaseRefined_0.9.db'

def get_articles(cluster_id):
    db = sqlite3.connect(DATABASE_NAME)
    c = db.cursor()
    q = "SELECT * FROM articles WHERE cluster=?"
    t = (cluster_id,)
    c.execute(q,t)
    articles = c.fetchall()
    return articles
