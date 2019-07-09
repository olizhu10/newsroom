from flask import Flask, render_template, request, send_file
from flask_socketio import SocketIO
import eventlet
import sqlite3
import database as db
from fragments import Fragments
import os
from metrics import cdplot, complot, create_matrix
import random
import io
import base64

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

@app.route('/plots/cd', methods=['POST'])
def show_cdplot():
    if request.method == 'POST':
        global cluster
        plot = cdplot(create_matrix(cluster))
        img = io.BytesIO()
        plot.savefig(img)
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plot.clf()
        return '<img src="data:image/png;base64,{}">'.format(plot_url)

@app.route('/plots/com', methods=['POST'])
def show_complot():
    if request.method == 'POST':
        global cluster
        plot = complot(create_matrix(cluster))
        img = io.BytesIO()
        plot.savefig(img)
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plot.clf()
        return '<img src="data:image/png;base64,{}">'.format(plot_url)

@socketio.on('send cluster')
def send_cluster():
    global cluster
    socketio.emit('cluster retrieved', cluster)

@socketio.on('send info')
def send_info(json):
    try:
        summary = json['summary']
        article = json['article']
        print(json)
        fragments = Fragments(cluster[int(summary)][1], cluster[int(article)][0])
        json = {'density': fragments.density(),
                'coverage': fragments.coverage(),
                'compression': fragments.compression(),
                'fragments': str(fragments.strings())}
        socketio.emit('info sent', json)
    except:
        pass

if __name__ == '__main__':
    socketio.run(app, debug=True)
