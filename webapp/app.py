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
        global cluster
        cluster = db.get_articles(cluster_id)
        return render_template('cluster.html', cluster=cluster)

@socketio.on('send summary cluster')
def send_cluster():
    socketio.emit('summary cluster retrieved', cluster)

@socketio.on('send article cluster')
def send_cluster():
    socketio.emit('article cluster retrieved', cluster)

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
