import jsonl
import numpy as np
from statistics import mean, median, stdev
import json
from fragments import Fragments
import csv
from tqdm import tqdm
from multiprocessing import Pool
with open('../clustering/articleSummaryPairsFinal.json', 'r') as file:
    pairs = json.load(file)

summaries_per_article = []

for pair in pairs:
    summary_list = pairs[pair]
    summaries_per_article.append(len(summary_list))

print("Average number of summaries per article: "+str(np.mean(summaries_per_article)))
print("Median number of summaries per article: "+str(np.median(summaries_per_article)))
print("Std of number of summaries per article: "+str(np.std(summaries_per_article)))
print("Minimum number of summaries per article: "+str(np.min(summaries_per_article)))
'''
with jsonl.open('../clustering/cluster_pairings.jsonl') as f:
    cluster_list = f.read()

cluster_lengths = []
summaries_per_article = []
num_articles_lt4 = []
num_clusters_lt4 = []

for cluster in cluster_list:
    cl = len(cluster)
    cluster_lengths.append(cl)
    if len(cluster) < 4:
        num_clusters_lt4.append(cl)
    for key in cluster:
        l = len(cluster[key])
        summaries_per_article.append(l)
        if l < 4:
            num_articles_lt4.append(l)

num_articles = np.sum(cluster_lengths)
avg_cluster_size = np.mean(cluster_lengths)
avg_summaries = np.mean(summaries_per_article)
print("Number of clusters: "+ str(len(cluster_lengths)))
print("Number of clusters with less than 4 articles: "+str(len(num_clusters_lt4)))
print("Number of articles: "+str(num_articles))
print("Average number of articles per cluster: "+str(np.mean(cluster_lengths)))
print("Average number of summaries per article: "+str(avg_summaries))
print("Median number of summaries per article: "+str(np.median(summaries_per_article)))
print("Std of number of summaries per article: "+str(np.std(summaries_per_article)))
print("Minimum number of summaries per article: "+str(np.min(summaries_per_article)))
'''
