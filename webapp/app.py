from flask import Flask, render_template
app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    with jsonl.open('../final_clusters.jsonl') as f:
        clusters = jsonl.read(f)
    cluster=clusters[500] #cluster index
    return render_template('index.html', cluster=cluster)

def submit_summary(s):

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
