import sqlite3
import pprint
import spacy
import jsonl
import json
import csv
import sys
import os
from tqdm import tqdm
from rouge import Rouge

with open('../clustering/summary_dict.json') as dictfile:
    summaryDict = json.load(dictfile)

def removeSummaries(threshold, type):
    with jsonl.open('../clustering/cluster_pairings.jsonl') as f:
        clusters = f.read()
    print('opened pairing file')
    cleaned_clusters = []
    print('beginning cluster cleaning')
    for cluster in tqdm(clusters, desc="clusters cleaned"):
        cleaned_articles = []
        for article in cluster:
            summaries = cluster[article]
            summary_texts = getSummaryTexts(summaries)
            ref_summary = summaryDict[article]
            cleaned_summaries = findGoodSummaries(ref_summary, summary_texts, threshold, type)
            if len(cleaned_summaries) >= 2:
                article_dict = {article: cleaned_summaries}
                cleaned_articles.append(article_dict)
        cleaned_clusters.append(cleaned_articles)
    print('finished cluster cleaning')
    with jsonl.open('../clustering/cluster_'+type+'_clean.jsonl') as outfile:
        for c in tqdm(cleaned_clusters, desc='adding clusters to file'):
            outfile.appendLine(c)
    return cleaned_clusters

def getSummaryTexts(summaries):
    texts = []
    for summary in summaries:
        texts.append(summaryDict[summary])
    return texts

def summaryDict():
    texts = {}
    db = sqlite3.connect('../databases/databaseRefined_0.9.db')
    c = db.cursor()
    q = 'SELECT summary, archive FROM articles'
    c.execute(q)
    summaries = c.fetchall()
    for summary in tqdm(summaries, desc='summaries added'):
        try:
            texts[summary[1]]
        except:
            texts[summary[1]] = summary[0]
    with open('../clustering/summary_dict.json', 'w+') as outfile:
        json.dump(texts, outfile)

def findGoodSummaries(ref_summary, summary_texts, threshold, type):
    good_summaries = []
    r = Rouge()
    for summary in summary_texts:
        score = r.get_scores(ref_summary, summary)[0][type]['f']
        if score > threshold:
            good_summaries.append(summary)
    return good_summaries

def main():
    threshold = float(sys.argv[1])
    type = sys.argv[2]
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(removeSummaries(threshold, type))

if __name__ == '__main__':
    main()
