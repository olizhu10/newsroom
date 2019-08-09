import sqlite3

def clean_articles(cluster_id):
    """cleans the articles from a certain cluster in the database in accordance to size"""
    db = sqlite3.connect('database.db')
    c = db.cursor()
    q = "SELECT text, archive FROM articles WHERE cluster=?"
    t = (cluster_id,)
    c.execute(q,t)
    articles = c.fetchall()
    text = ""
    count = 0
    for a in articles:
        if (text != a[0]):
            text = a[0]
            q = "DELETE FROM articles WHERE archive = ? AND cluster=?"
            t = (a[1], cluster_id)
            c.execute(q,t)
        else:
            count += 1
    if count <= 3:
        q = "DELETE FROM articles WHERE cluster=?"
        t = (cluster_id,)
        c.execute(q,t)


if __name__ == '__main__':
    for i in range(15742):
        clean_articles(i)
        print(i)
