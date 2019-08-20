import sqlite3
import pprint
import spacy
import jsonl
import csv
import sys
import smd
import os
from tqdm import tqdm

print('loading spacy')
nlp = spacy.load('en_core_web_md')

def removeSummaries(threshold):
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
            ref_summary = summary_texts[article][0]
            write_wsms_input(ref_summary, summary_texts)
            #os.system("python smd.py ../data/sms_input.tsv glove s+wms")
            smd.main('../data/sms_input.tsv', 'glove', 's+wms', nlp)
            cleaned_summaries = findGoodSummaries(ref_summary, summary_texts, threshold)
            if len(cleaned_summaries) >= 2:
                article_dict = {article: cleaned_summaries}
                cleaned_articles.append(article_dict)
        cleaned_clusters.append(cleaned_articles)
    print('finished cluster cleaning')
    with jsonl.open('../clustering/cluster_wsms_clean.jsonl') as outfile:
        for c in tqdm(cleaned_clusters, desc='adding clusters to file'):
            outfile.appendLine(c)
    return cleaned_clusters

def getSummaryTexts(summaries):
    texts = {}
    for archive in summaries:
        db = sqlite3.connect('../databases/databaseRefined_0.9.db')
        c = db.cursor()
        q = 'SELECT summary FROM articles WHERE archive=?'
        t = (archive,)
        c.execute(q,t)
        summary = c.fetchone()
        texts[archive] = summary
    return texts

def findGoodSummaries(ref_summary, summary_texts, threshold):
    good_summaries = []
    with open('../data/sms_input_glove_s+wms.out') as f:
        reader = list(csv.reader(f, delimiter='\t'))
        line = 2
        while line < len(summary_texts)+2:
            score = float(reader[line][3])
            if score > threshold:
                summary = reader[line][2]
                good_summaries.append(summary)
            line += 1
    return good_summaries

def write_wsms_input(ref_summary, summaries):
    with open('../data/sms_input.tsv', 'w+') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t')
        for summary in summaries:
            row = [ref_summary, summaries[summary][0]]
            writer.writerow(row)

def main(threshold):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(removeSummaries(threshold))

if __name__ == '__main__':
    threshold = float(sys.argv[1])
    main(threshold)
