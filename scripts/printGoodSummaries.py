import sys
import jsonl
from multiprocessing import Pool
from threading import Lock
from tqdm import tqdm
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import json
def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent

with open('../clustering/articleSummaryPairs.json') as f:
    articleListing = json.load(f)
with jsonl.open('../dataset_files/train.jsonl.gz', gzip=True) as ds:
    articles = ds.read()

def createDictionary():
    '''creates a dictionary mapping the archive link to (summary, text) tuple'''
    dict = {}
    pbar = tqdm(total=len(articles), desc='Generating Dictionary:')
    for article in articles:
        dict[article['archive']]=(article['summary'],article['text'])
        pbar.update(1)
    return dict

def main():
    '''prints the good article summary pairs which are left'''
    dict = createDictionary()
    for article in articleListing:
        for summary in articleListing[article]:
            print(dict[summary][0])
        print("")

if __name__ == '__main__':
    main()
