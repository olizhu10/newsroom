import sqlite3 as sql


def get_cluster(index):
    db = sqlite3.connect(DATABASE_NAME)
    c = db.cursor()
    q = 'SELECT text, summary, title, archive FROM articles WHERE cluster = ?'
    t = (index, )
    c.execute(q, t)
    results = c.fetchall()
    return results
