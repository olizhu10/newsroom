from flask import Flask, render_template, request
from flask_socketio import SocketIO
import eventlet
import sqlite3
import database as db

app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app)
cluster = []

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/cluster', methods=['POST', 'GET'])
def get_cluster():
    if request.method == 'POST':
        cluster_id = request.form['cluster']
        cluster = db.get_articles(cluster_id)
        json = { cluster: cluster}
        socketio.emit('cluster retrieved', cluster)
        return render_template('cluster.html', cluster=cluster)

@app.route('/article', methods=['POST'])
def get_article():
    if request.method == 'POST':
        text = request.form['article-submit']
        json = {'text': text}
    socketio.emit('article selected', json)
    return render_template('article.html', article=text)

@app.route('/summary', methods=['POST', 'GET'])
def get_summary():
    if request.method == 'POST':
        index = int(request.form['summary-submit'])
        f = request.form
        for key in f.keys():
            for value in f.getlist(key):
                print(key,":",value)
        print(cluster)
        text = cluster[index]
    return render_template('summary.html', cluster=cluster, summary=text, article=text)

if __name__ == '__main__':
    socketio.run(app, debug=True)
