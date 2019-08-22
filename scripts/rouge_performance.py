import concurrent.futures
import sqlite3
import pprint
import spacy
import jsonl
import json
import csv
import sys
import os
import numpy as np
from tqdm import tqdm
from rouge import Rouge
from multiprocessing import Pool

def removeSummaries(key):
    threshold = 0.15
    type='rouge-l'
    summaries = articles[key]
    summary_texts, ref_summary = getSummaryTexts(summaries, key)
    cleaned_summaries = findGoodSummaries(ref_summary, summary_texts)
    return cleaned_summaries, key

def getSummaryTexts(summaries, article):
    texts = []
    ref_summary = ""
    for summary in summaries:
        if summary == article:
            ref_summary = summary_dict[summary]
        if not summary in texts:
            texts.append(summary_dict[summary])
    return texts, ref_summary

def summaryDict():
    texts = {}
    with jsonl.open('../dataset_files/train.jsonl.gz', gzip=True) as ds:
        articles = ds.read()

    summaries = []
    for article in articles:
        summaries.append((article['summary'], article['archive']))

    for summary in tqdm(summaries, desc='summaries added'):
        try:
            texts[summary[1]]
        except:
            texts[summary[1]] = summary[0]

    with open('../clustering/summary_dict.json', 'w+') as outfile:
        json.dump(texts, outfile)

def findGoodSummaries(ref_summary, summary_texts):
    threshold = 0.25
    type = 'rouge-1'
    good_summaries = []
    r = Rouge()
    for summary in summary_texts:
        try:
            score = r.get_scores(ref_summary, summary, ignore_empty=True)[0][type]['f']
            if score > threshold:
                good_summaries.append(summary)
        except ValueError:
            print('this pair had an invalid input\nref summary: '+ref_summary+'\nsummary: '+summary)
    return good_summaries

def printNumArticles(type):
    with open('../clustering/aspair_'+type+'.json') as f:
        articles = json.load(f)
    arts = len(articles)
    sums = []
    for key in articles:
        sums.append(len(articles[key]))
    print('num articles: '+str(arts)+'\nnum summaries: '+str(np.sum(sums))+
        '\navg # summaries per article: '+str(np.mean(sums)))

if __name__ == '__main__':

    with open('../clustering/summary_dict.json') as dictfile:
        summary_dict = json.load(dictfile)
    with open('../clustering/articleSummaryPairsFinal.json') as f:
        articles = json.load(f)
    print('opened pairing file')

    cleaned_articles = {}
    args = []
    for article in articles:
        args.append((article, cleaned_articles))

    print('beginning cluster cleaning')
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
    print(str(0.25))

    with open('../clustering/rouge1_article_summary_pairs0.25.json', 'w+') as f:
        json.dump(cleaned_articles, f)
