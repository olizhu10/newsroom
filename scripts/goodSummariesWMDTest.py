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
thresholds = [0.65]
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
    summaryTextList = []
    tp = [0]
    tn = [0]
    fp = [0]
    fn = [0]
    for article in clusters[x]:
        #if(len(preprocess(dict[article][1]))>=50 and len(preprocess(dict[article][0]))>=5):
        articleList.append(dict[article][1])
        summaryList.append(dict[article][0])
        summaryWMDList.append(nlp(dict[article][1]))
        summaryTextList.append(dict[article][0])
    articleList = fullListList(articleList)
    summaryList = namesListList(summaryList)
    for aIndex, article in enumerate(articleList, start = 0):
        summaries = []
        for sIndex, summary in enumerate(summaryList, start = 0):
            if(nameDifferences(summary, article) or aIndex == sIndex):
                summaries.append(clusters[x][sIndex])
                if (aIndex != sIndex):
                    simMeasure = summaryWMDList[aIndex].similarity(summaryWMDList[sIndex])
                    for i in range(1):
                        if(simMeasure>thresholds[i]):
                            tp[i] += 1
                        else:
                            fn[i] += 1
                            print("article summary:" +summaryTextList[aIndex])
                            print("summary summary:" +summaryTextList[sIndex])
            else:
                simMeasure = summaryWMDList[aIndex].similarity(summaryWMDList[sIndex])
                for i in range(1):
                    if(simMeasure<thresholds[i]):
                        tn[i] += 1
                    else:
                        fp[i] += 1
        if len(summaries)>=4:
            smallDict[clusters[x][aIndex]] = summaries
    return (tp, tn, fp, fn)

def main():
    articleDict = {}
    pbar = tqdm(total=len(clusters), desc='Going through Clusters:')
    count = 0
    tp = [0]
    tn = [0]
    fp = [0]
    fn = [0]
    with Pool(processes=15) as pool:
        for results in pool.imap_unordered(analyzeCluster, range(len(clusters))):
            for i in range(1):
                tp[i] += results[0][i]
                tn[i] += results[1][i]
                fp[i] += results[2][i]
                fn[i] += results[3][i]
            pbar.update(1)
    print(tp)
    print(tn)
    print(fp)
    print(fn)

if __name__ == '__main__':
    main()
