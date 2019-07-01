from flask import Flask, render_template, request
from flask_socketio import SocketIO
import eventlet
import sqlite3
import database as db

app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('base.html')

#@socketio.on('cluster id submitted')
@app.route('/cluster', methods=['POST'])
def get_cluster():
    if request.method == 'POST':
        #cluster_id = json[cluster_id]
        cluster_id = request.form['cluster']
        print(cluster_id)
        cluster = db.get_articles(cluster_id)
        return render_template('cluster.html', cluster=cluster)

if __name__ == '__main__':
    socketio.run(app, debug=True)
