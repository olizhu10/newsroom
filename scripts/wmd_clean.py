import numpy as np
import spacy
import jsonl
import wmd
import gensim
import pprint
from tqdm import tqdm
from gensim.models import Word2Vec
from nltk.tokenize import sent_tokenize, word_tokenize

nlp = spacy.load('en_core_web_lg')

def createDictionary():
    with jsonl.open('../dataset_files/train.jsonl.gz', gzip=True) as ds:
        articles = ds.read()
    dict = {}
    pbar = tqdm(total=len(articles), desc='Generating Dictionary:')
    for article in articles:
        dict[article['archive']]=(article['text'], article['summary'])
        pbar.update(1)
    return dict

def clean():
    with jsonl.open('../clustering/final_clusters_cleaned0.9_2.jsonl') as file:
        clusters = file.read()

    for cluster in clusters:
        clean_by_sim(cluster)

def article_sims(cluster, dict):
    cluster_sims = []
    for article in cluster:
        doc = nlp(dict[article][0])
        sims = []
        for x in cluster:
            docx = nlp(dict[x][0])
            sim = doc.similarity(docx)
            sims.append(sim)
        cluster_sims.append(sims)
    return cluster_sims

def summary_sims(cluster, dict):
    cluster_sims = []
    for article in cluster:
        doc = nlp(dict[article][1])
        sims = []
        for x in cluster:
            docx = nlp(dict[x][1])
            sim = doc.similarity(docx)
            sims.append(sim)
        cluster_sims.append(sims)
    return cluster_sims

def test():
    dict = createDictionary()
    with jsonl.open('../clustering/final_clusters_cleaned0.9_2.jsonl') as file:
        clusters = file.read()
    cluster = clusters[4389]
    np.set_printoptions(linewidth=500, precision=3, threshold=100000)
    print(np.array(article_sims(cluster,dict)))
    print(np.array(summary_sims(cluster,dict)))

if __name__ == '__main__':
    test()
