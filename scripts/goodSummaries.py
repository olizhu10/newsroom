import sys
import jsonl
from multiprocessing import Pool
from threading import Lock
from tqdm import tqdm
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent

with jsonl.open('../clustering/final_clusters_cleaned0.9_2.jsonl') as f:
    clusters = f.read()
with jsonl.open('../dataset_files/train.jsonl.gz', gzip=True) as ds:
    articles = ds.read()

def createDictionary():
    dict = {}
    pbar = tqdm(total=len(articles), desc='Generating Dictionary:')
    for article in articles:
        dict[article['archive']]=(article['summary'],article['text'])
        pbar.update(1)
    return dict

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
            return False
    return True

def main():
    dict = createDictionary()
    articleDict = {}
    count = 0
    for cluster in clusters:
        for article in cluster:
            summaries = []
            for article_alt in cluster:
                if(nameDifferences(dict[article_alt][0], dict[article][1])):
                    summaries.append(article_alt)
            if len(summaries)>=4:
                articleDict[article] = summaries
                count += 1
    json.dump(dict,'../clustering/articleSummaryPairs.json')
    print("Count" + count)

if __name__ == '__main__':
    main()
