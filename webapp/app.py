from flask import Flask, render_template, request, send_file
from flask_socketio import SocketIO
import eventlet
import sqlite3
import database as db
from fragments import Fragments
import os
from metrics import cdplot, complot
from ASData import ASData
import random
import io

app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('base.html', last_updated=dir_last_updated('static'))

def dir_last_updated(folder):
    return str(max(os.path.getmtime(os.path.join(root_path, f))
               for root_path, dirs, files in os.walk(folder)
               for f in files))

@app.route('/cluster', methods=['POST', 'GET'])
def get_cluster():
    if request.method == 'POST':
        cluster_id = request.form['cluster']
        global cluster
        cluster = db.get_articles(cluster_id)
        return render_template('cluster.html', cluster=cluster, last_updated=dir_last_updated('static'),
            val=cluster_id)

@app.route('/rand-cluster', methods=['POST','GET'])
def get_rand_cluster():
    if request.method == 'POST':
        cluster_id = random.randint(0,15741)
        global cluster
        cluster = db.get_articles(cluster_id)
        return render_template('cluster.html', cluster=cluster, last_updated=dir_last_updated('static'),
            val=cluster_id)

@app.route('/cd_plot')
def cd_plot():
    global cluster
    plot = cdplot(create_matrix(cluster))
    img = io.BytesIO()
    plot.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')

@app.route('/plots/cd', methods=['POST'])
def show_cdplot():
    return render_template('cdplot.html')

@app.route('/com_plot')
def com_plot():
    plot = complot(create_matrix(cluster))
    img = io.BytesIO()
    plot.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')

@app.route('/plots/com', methods=['POST'])
def show_complot():
    return render_template('complot.html')

@socketio.on('send cluster')
def send_cluster():
    global cluster
    socketio.emit('cluster retrieved', cluster)

@socketio.on('send info')
def send_info(json):
    try:
        summary = json['summary']
        article = json['article']
        print('working'+str(json))
        fragments = Fragments(cluster[int(summary)][1], cluster[int(article)][0])
        json = {'density': fragments.density(),
                'coverage': fragments.coverage(),
                'compression': fragments.compression()}
        socketio.emit('info sent', json)
    except:
        pass

def create_matrix(cluster):
    articles = []
    summaries = []
    for article in cluster:
        articles.append(article)
        summaries.append(article[1])

    matrix = []
    num = 0
    for article in articles:
        text = article[0]
        title = article[2]
        entries = []
        for index in range(len(summaries)):
            summary = summaries[index]
            fragments = Fragments(summary, text)
            obj = ASData(article, summary, title, True, fragments.coverage(),
                fragments.density(), fragments.compression())
            entries.append(obj)
        matrix.append(entries)
        num += 1
    return matrix

if __name__ == '__main__':
    socketio.run(app, debug=True)
