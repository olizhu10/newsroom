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
    threshold = 0.02
    summaries = articles[key]
    ref_summary = summary_dict[key]
    summary_texts, inputs = getSummaryTexts(summaries, ref_summary, key)
    cleaned_summaries = findGoodSummaries(ref_summary, summary_texts, threshold)
    return cleaned_summaries, key

def getSummaryTexts(summaries, ref_summary, article):
    texts = []
    inputs = []
    for summary in summaries:
        summary_text = summary_dict[summary]
        if not summary in texts:
            texts.append(summary_text)
            inputs.append([ref_summary, summary_text])
    return texts, inputs

def findGoodSummaries(ref_summary, summary_texts, threshold):
    good_summaries = []
    for summary in summary_texts:
        score = calc_smd([ref_summary, summary], nlp)
        if score[0] > threshold:
            good_summaries.append(summary)
    #for dict in scores:
    #    if dict['score'] > threshold:
    #        good_summaries.append(dict['hyp'])
    return good_summaries


if __name__ == '__main__':
    with open('../clustering/summary_dict.json') as dictfile:
        summary_dict = json.load(dictfile)
    with open('../clustering/articleSummaryPairsFinal.json') as f:
        articles = json.load(f)
    print('opened pairing and summary files')

    cleaned_articles = {}
    print('beginning article cleaning')
    pbar = tqdm(total=len(articles), desc="articles cleaned")
    with Pool() as pool:
        for cleaned_summaries, key in pool.imap_unordered(removeSummaries, articles):
            if len(cleaned_summaries) >= 2:
                for summary in cleaned_summaries:
                    if key in cleaned_articles.keys():
                        if not (summary in cleaned_articles[key]):
                            cleaned_articles[key].append(summary)
                    else:
                        cleaned_articles[key] = cleaned_summaries
            pbar.update(1)

    arts = len(cleaned_articles)
    sums = []
    for key in cleaned_articles:
        sums.append(len(articles[key]))
    print('num articles: '+str(arts)+'\nnum summaries: '+str(np.sum(sums))+
        '\navg # summaries per article: '+str(np.mean(sums)))
    print(str(0.02))
