import sqlite3

def get_articles(cluster_id):
    db = sqlite3.connect('databaseRefined.db')
    c = db.cursor()
    q = "SELECT * FROM articles WHERE cluster=?"
    t = (cluster_id,)
    c.execute(q,t)
    articles = c.fetchall()
    return articles
