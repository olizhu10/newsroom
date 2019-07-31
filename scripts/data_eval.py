import jsonl
import numpy as np
from statistics import mean, median, stdev
import json
from fragments import Fragments
import matplotlib.pyplot as plt

"""
Prints statistics for number of summaries per article.
"""

with open('../clustering/articleSummaryPairsFinal.json', 'r') as file:
    pairs = json.load(file)

summaries_per_article = []
for pair in pairs:
    summary_list = pairs[pair]
    summaries_per_article.append(len(summary_list))

spa_lt20 = []
for x in summaries_per_article:
    if x <= 20:
        spa_lt20.append(x)

print("Average number of summaries per article: "+str(np.mean(summaries_per_article)))
print("Median number of summaries per article: "+str(np.median(summaries_per_article)))
print("Std of number of summaries per article: "+str(np.std(summaries_per_article)))
print("Minimum number of summaries per article: "+str(np.min(summaries_per_article)))

def plot():
    plt.xlabel('number of summaries per article')
    plt.ylabel('frequency')
    plt.hist(spa_lt20)
    plt.show()

plot()
