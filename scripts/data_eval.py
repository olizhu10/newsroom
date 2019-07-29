import jsonl
import numpy as np
from statistics import mean, median, stdev
import json
from fragments import Fragments
import csv
from tqdm import tqdm
from multiprocessing import Pool

"""
Prints statistics for number of summaries per article.
"""

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
