from flask import Flask, render_template, request
from flask_socketio import SocketIO
import eventlet
import sqlite3
import database as db
from fragments import Fragments
import os

app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app)
cluster = []

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
        return render_template('cluster.html', cluster=cluster, last_updated=dir_last_updated('static'))

@socketio.on('send cluster')
def send_summary_cluster():
    socketio.emit('cluster retrieved', cluster)

@socketio.on('send info')
def send_info(json):
    try:
        summary = json['summary']
        article = json['article']
        print(json)
        global cluster
        fragments = Fragments(cluster[int(summary)][1], cluster[int(article)][0])
        json = {'density': fragments.density(),
                'coverage': fragments.coverage(),
                'compression': fragments.compression()}
        socketio.emit('info sent', json)
    except:
        pass

@socketio.on('create plot')
def create_plot():
    colors = ['red','blue','pink','yellow','black','orange','purple','green','cyan',
    'magenta','grey']
    plt.title(event)
    plt.xlabel('coverage')
    plt.ylabel('density')

    coverages = []
    densities = []
    for x in range(len(cluster)):
        title = cluster[x][2]
    
    for x in range(len(matrix)):
        coverages = []
        densities = []
        title = matrix[x][0].getTitle()[:20]
        for obj in matrix[x]:
            if obj.getMatch() == True:
                coverages.append(obj.getCoverage())
                densities.append(obj.getDensity())
        plt.scatter(coverages, densities, marker = 'o', c=colors[x], label=title, alpha=0.6)
    plt.legend()
    plt.savefig('../events/data/'+event+'.png')
    plt.show()
if __name__ == '__main__':
    socketio.run(app, debug=True)
