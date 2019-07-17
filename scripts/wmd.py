import numpy
import spacy
import jsonl
from nltk.corpus import stopwords
from nltk import download
from gensim.models import Word2Vec
from gensim.similarities import WmdSimilarity
download('stopwords')

with jsonl.open('../clustering/final_clusters_0.9_cleaned') as file:
    clusters = file.read()

with jsonl.open('../dataset_files/train.jsonl.gz', gzip = True) as file:
    data = file.read()

def similarities():
    stop_words = stopwords.words('english')
    model = Word2Vec.load_word2vec_format('../w2v_googlenews/GoogleNews-vectors-negative300.bin.gz', binary=True)
    model.save('w2v_google.model')
    keyed = model.wv #contains the word mapping vectors

    for cluster in clusters:
        preprocessed = []
        for article in cluster:
            preprocessed.append(preprocess(get_text(article)))
        for article in cluster:
            distances = []
            for x in cluster:
                if x != article:
                    distance = model.wmdistance(article,x)
                    distances.append(distance)
            avg_dis = numpy.mean(distances)
            if avg_dis > __:
                #remove from cluster

def get_text(archive):
    for article in data:
        if article['archive'] == archive:
            return article['text']
        else:
            raise error

def preprocess(doc):
    doc = doc.lower()  # Lower the text.
    doc = word_tokenize(doc)  # Split into words.
    doc = [w for w in doc if not w in stop_words]  # Remove stopwords.
    doc = [w for w in doc if w.isalpha()]  # Remove numbers and punctuation.
    return doc
