#!/usr/bin/env python3
from flask import Flask, render_template, request, send_file, redirect, url_for
import eventlet
import sqlite3
import database as db
from fragments import Fragments
import os
from plot import cdplot, complot
import random
import io
import base64
import sys
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
#nltk.download("punkt")
#nltk.download('averaged_perceptron_tagger')

app = Flask(__name__, template_folder='templates')
clusters = {}

@app.route('/')
def index():
    return render_template('base.html', last_updated=dir_last_updated('static'))

@app.route('/<cluster_id>/<message>')
def home(cluster_id, message):
    print(message)
    return render_template('base.html', last_updated=dir_last_updated('static'),
        message=message)

@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        cluster_id = request.form['cluster']
        if cluster_id == '':
            message = "Please enter a valid cluster index."
            return redirect(url_for('home', cluster_id=0, message=message))
        return redirect(url_for('get_cluster', cluster_id=cluster_id))

@app.route('/random', methods=['POST'])
def random_cluster():
    if request.method == 'POST':
        cluster_id = random.randint(0,13487)
        return redirect(url_for('get_cluster', cluster_id=cluster_id))

@app.route('/cluster/<int:cluster_id>', methods=['POST','GET'])
def get_cluster(cluster_id):
    clusters[request.remote_addr] = db.get_articles(cluster_id)
    cluster = clusters[request.remote_addr]
    if cluster == []:
        message= "The cluster you searched for doesn't exist. Please select a new one."
        return redirect(url_for('home', cluster_id=cluster_id, message=message))
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
        val=cluster_id, summary_text=json['annotation'][0], article_text=json['annotation'][1],
        density=json['density'], coverage=json['coverage'], compression=json['compression'],
        fragments=json['fragments'], diffNames = nameDifferences(str(summary_text), str(article_text)),
        summary=summary, article=article)

@app.route('/cdplot', methods=['POST'])
def cd_plot():
    if request.method == 'POST':
        if sys.platform == 'darwin':
            return '<p>Plots cannot be generated on Mac OS X. sorry :(</p>'
        else:
            cluster_id = request.form['cid']
            return redirect(url_for('make_plot', type='cd', cluster_id=cluster_id))

@app.route('/complot', methods=['POST'])
def com_plot():
    if request.method == 'POST':
        if sys.platform == 'darwin':
            return '<p>Plots cannot be generated on Mac OS X. sorry :(</p>'
        else:
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
    plot.savefig(img, bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plot.clf()
    return '<img src="data:image/png;base64,{}">'.format(plot_url)

@app.route('/remove', methods=['POST'])
def remove_cluster():
    if request.method == 'POST':
        cluster_id = request.form['cid']
        db.remove_cluster(cluster_id)
        message="Cluster Removed"
        return redirect(url_for('home',message=message))

@app.route('/confirm/<int:cluster_id>', methods=['GET','POST'])
def confirm(cluster_id):
    return render_template('remove.html', cluster_id)

def dir_last_updated(folder):
    return str(max(os.path.getmtime(os.path.join(root_path, f))
               for root_path, dirs, files in os.walk(folder)
               for f in files))

def get_info(summary, article):

    cluster = clusters[request.remote_addr]
    fragments = Fragments(cluster[int(summary)][1], cluster[int(article)][0])
    string_frags = []
    for frag in fragments.strings():
        string_frags.append(str(frag))
    json = {'annotation': fragments.annotate(),
            'density': fragments.density(),
            'coverage': fragments.coverage(),
            'compression': fragments.compression(),
            'fragments': fragments.annotate_fragments()}
    return json


def preprocess(sent):
    return nltk.pos_tag(nltk.word_tokenize(sent))

def namesList(sentence):
    nList = []
    for word in preprocess(sentence):
        if word[1]=="NNP":
            nList.append(word[0])
    return nList

def nameDifferences(summary, article):
    diffList = []
    aList = namesList(article)
    for word in namesList(summary):
        if not (word in aList) and not (word in diffList):
            diffList.append(word)
    return diffList

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug=True)
