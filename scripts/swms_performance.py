import concurrent.futures
import sqlite3
import pprint
import string
import spacy
import jsonl
import json
import csv
import sys
import os
import re
import numpy as np
from tqdm import tqdm
from smd import calc_smd
from multiprocessing import Pool

nlp = spacy.load('en_core_web_md')
print('spacy loaded')

def removeSummaries(key):
    summaries = articles[key]
    ref_summary = summary_dict[key]
    inputs = getSummaryTexts(summaries, ref_summary)
    #print(inputs)
    scores = calc_smd(inputs, nlp)
    return findGoodSummaries(ref_summary, scores), key

def getSummaryTexts(summaries, ref_summary):
    #texts = []
    inputs = []
    for summary in summaries:
        summary_text = summary_dict[summary]
        #texts.append(summary_text)
        inputs.append([ref_summary, summary_text])
    return inputs

def findGoodSummaries(ref_summary, scores):
    good_summaries001 = []
    good_summaries002 = []
    good_summaries003 = []
    for dict in scores:
        score = dict['score']
        summary = dict['hyp']
        if score > 0.03:
            good_summaries003.append(summary)
        if score > 0.02:
            good_summaries002.append(summary)
        if score > 0.01:
            good_summaries001.append(summary)
    return [good_summaries001, good_summaries002, good_summaries003]


if __name__ == '__main__':
    with open('../clustering/summary_dict.json') as dictfile:
        summary_dict = json.load(dictfile)
    with open('../clustering/articleSummaryPairsFinal.json') as f:
        articles = json.load(f)
    print('opened pairing and summary files')

    cleaned_articles = [{},{},{}]
    print('beginning article cleaning')
    '''
    for key in tqdm(list(articles.keys())[2195:],desc="articles cleaned"):
        summary_sets, _ = removeSummaries(key)
        for i in range(len(summary_sets)):
            if len(summary_sets[i]) >= 2:
                for summary in summary_sets[i]:
                    if key in cleaned_articles[i].keys():
                        if not (summary in cleaned_articles[i][key]):
                            cleaned_articles[i][key].append(summary)
                    else:
                        cleaned_articles[i][key] = summary_sets[i]
    '''

    pbar = tqdm(total=len(list(articles.keys())), desc="articles cleaned")
    with Pool() as pool:
        for summary_sets, key in pool.imap_unordered(removeSummaries, articles):
            for i in range(len(summary_sets)):
                if len(summary_sets[i]) >= 2:
                    for summary in summary_sets[i]:
                        if key in cleaned_articles[i].keys():
                            if not (summary in cleaned_articles[i][key]):
                                cleaned_articles[i][key].append(summary)
                        else:
                            cleaned_articles[i][key] = summary_sets[i]
            pbar.update(1)

    for i in range(len(cleaned_articles)):
        arts = len(cleaned_articles[i])
        print('set: '+str(i))
        sums = []
        for key in cleaned_articles[i]:
            sums.append(len(cleaned_articles[i][key]))
        print('num articles: '+str(arts)+'\nnum summaries: '+str(np.sum(sums))+
            '\navg # summaries per article: '+str(np.mean(sums)))

    with jsonl.open('swms_article_summary_pairs.json', 'w+') as f:
        f.write(cleaned_articles)
