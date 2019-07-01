from flask import Flask, render_template
from flask_socketio import SocketIO
import eventlet
import sqlite3
import webapp.database as db

app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('base.html')

@socketio.on('cluster id submitted')
def get_cluster(json):
    cluster = db.get_articles(json[cluster_id])
    return render_template('cluster.html', cluster=cluster)

if __name__ == '__main__':
    socketio.run(app, debug=True)
