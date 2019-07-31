import sys
import jsonl
from multiprocessing import Pool
from threading import Lock
from tqdm import tqdm
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import json
import spacy
import wmd

nlp = spacy.load('en', create_pipeline=wmd.WMD.create_spacy_pipeline)
#nlp = spacy.load('en_core_web_lg')
def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent

with jsonl.open('../clustering/final_clusters_cleaned0.9_2.jsonl') as f:
    clusters = f.read()
with jsonl.open('../dataset_files/train.jsonl.gz', gzip=True) as ds:
    articles = ds.read()

def createDictionary():
    """Creates dictionary for entire dataset with article archives as keys and
    (summary, text) as values."""
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
            nList.append(word[0].lower())
    return nList

def fullList(sentence):
    nList = []
    for word in preprocess(sentence):
        nList.append(word[0].lower())
    return nList
def nameDifferences(summaryList, articleList):
    diffList = []
    for word in summaryList:
        if not (word in articleList):
            return False
    return True

def namesListList(list):
    nList = []
    for sentence in list:
        nList.append(namesList(sentence))
    return nList

def fullListList(list):
    nList = []
    for sentence in list:
        nList.append(fullList(sentence))
    return nList

dict = createDictionary()
def analyzeCluster(x):
    smallDict = {}
    articleList = []
    summaryList = []
    summaryWMDList = []
    for article in clusters[x]:
        if(len(preprocess(dict[article][1]))>=50 and len(preprocess(dict[article][0]))>=5):
            articleList.append(dict[article][1])
            summaryList.append(dict[article][0])
            summaryWMDList.append(nlp(dict[article][1]))
    articleList = fullListList(articleList)
    summaryList = namesListList(summaryList)
    for aIndex, article in enumerate(articleList, start = 0):
        summaries = []
        for sIndex, summary in enumerate(summaryList, start = 0):
            simMeasure = summaryWMDList[aIndex].similarity(summaryWMDList[sIndex])
            if((nameDifferences(summary, article) or aIndex == sIndex) and simMeasure > 0.85):
                summaries.append(clusters[x][sIndex])
        if len(summaries)>=4:
            smallDict[clusters[x][aIndex]] = summaries
    return smallDict

def main():
    articleDict = {}
    pbar = tqdm(total=len(clusters), desc='Going through Clusters:')
    count = 0
    with Pool(processes=15) as pool:
        for smallDict in pool.imap_unordered(analyzeCluster, range(len(clusters))):
            for key in smallDict:
                if key in articleDict:
                    for summary in smallDict[key]:
                        if not summary in articleDict[key]:
                            articleDict[key].append(summary)
                else:
                    articleDict[key] = smallDict[key]
                    count += 1
            pbar.update(1)
    print(count)
    with open('../clustering/articleSummaryPairsWMDShave.json', 'w+') as file:
        json.dump(articleDict, file)
if __name__ == '__main__':
    main()
