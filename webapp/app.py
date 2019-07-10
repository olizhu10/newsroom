#!/usr/bin/env python3
from flask import Flask, render_template, request, send_file, redirect, url_for
from flask_socketio import SocketIO
import eventlet
import sqlite3
import database as db
from fragments import Fragments
import os
from plot import cdplot, complot
import random
import io
import base64

app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app)
clusters = {}

@app.route('/')
def index():
    return render_template('base.html', last_updated=dir_last_updated('static'))

def dir_last_updated(folder):
    return str(max(os.path.getmtime(os.path.join(root_path, f))
               for root_path, dirs, files in os.walk(folder)
               for f in files))

@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        cluster_id = request.form['cluster']
        return redirect(url_for('get_cluster', cluster_id=cluster_id))

@app.route('/random', methods=['POST'])
def random_cluster():
    if request.method == 'POST':
        cluster_id = random.randint(0,12987)
        return redirect(url_for('get_cluster', cluster_id=cluster_id))

@app.route('/cluster/<int:cluster_id>', methods=['POST','GET'])
def get_cluster(cluster_id):
    clusters[request.remote_addr] = db.get_articles(cluster_id)
    cluster = clusters[request.remote_addr]
    return render_template('cluster.html', cluster=cluster, last_updated=dir_last_updated('static'),
        val=cluster_id, summary_text="No summary selected.", article_text="No article selected.")

@app.route('/select', methods=['POST'])
def select():
    if request.method == 'POST':
        summary = request.form['summary-select']
        article = request.form['article-select']
        cluster_id = request.form['cid']
        return redirect(url_for('get_text', summary=summary, article=article,
            cluster_id=cluster_id))

@app.route('/cluster/<int:cluster_id>/<int:summary>/<int:article>', methods=['POST','GET'])
def get_text(cluster_id, summary, article):
    try:
        cluster = clusters[request.remote_addr]
    except:
        clusters[request.remote_addr] = db.get_articles(cluster_id)
        cluster = clusters[request.remote_addr]
    summary_text = cluster[summary][1]
    article_text = cluster[article][0]
    json = get_info(summary, article)
    return render_template('cluster.html', cluster=cluster, last_updated=dir_last_updated('static'),
        val=cluster_id, summary_text=summary_text, article_text=article_text,
        density=json['density'], coverage=json['coverage'], compression=json['compression'],
        fragments=json['fragments'], summary=summary, article=article)

@app.route('/cdplot', methods=['POST'])
def cd_plot():
    if request.method == 'POST':
        cluster_id = request.form['cid']
        return redirect(url_for('make_plot', type='cd', cluster_id=cluster_id))

@app.route('/complot', methods=['POST'])
def com_plot():
    if request.method == 'POST':
        cluster_id = request.form['cid']
        return redirect(url_for('make_plot', type='com', cluster_id=cluster_id))

@app.route('/cluster/<int:cluster_id>/<type>', methods=['GET','POST'])
def make_plot(type, cluster_id):
    cluster = clusters[request.remote_addr]
    if type == 'cd':
        plot = cdplot(cluster)
    else:
        plot = complot(cluster)
    img = io.BytesIO()
    plot.savefig(img)
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plot.clf()
    return '<img src="data:image/png;base64,{}">'.format(plot_url)

@socketio.on('send cluster')
def send_cluster():
    try:
        cluster = clusters[request.remote_addr]
    except:
        clusters[request.remote_addr] = db.get_articles(cluster_id)
        cluster = clusters[request.remote_addr]
    socketio.emit('cluster retrieved', cluster)

def get_info(summary, article):
    try:
        cluster = clusters[request.remote_addr]
        fragments = Fragments(cluster[int(summary)][1], cluster[int(article)][0])
        json = {'density': fragments.density(),
                'coverage': fragments.coverage(),
                'compression': fragments.compression(),
                'fragments': str(fragments.strings())}
        return json
    except:
        pass

if __name__ == '__main__':
    socketio.run(app, host = '0.0.0.0', port = 5000, debug=True)
