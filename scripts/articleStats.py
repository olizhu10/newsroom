from statistics import mean, median, stdev
import json
from fragments import Fragments
import csv
from tqdm import tqdm
from multiprocessing import Pool
import jsonl
with open('../clustering/articleSummaryPairsFinal.json', 'r') as file:
    pairs = json.load(file)
print("Pairs Loaded")
with jsonl.open('../dataset_files/train.jsonl.gz', gzip=True) as ds:
    articles = ds.read()

print("Articles Loaded")
def createDictionary():
    dict = {}
    pbar = tqdm(total=len(articles), desc='Generating Dictionary:')
    for article in articles:
        dict[article['archive']]=(article['summary'],article['text'])
        pbar.update(1)
    return dict

dict = createDictionary()
articleList = []
for article in pairs:
    articleList.append(article)
print("Dictionary Created")

def analyzeArticle(x):
    compressions = []
    densities = []
    coverages = []
    text = dict[articleList[x]][1]
    for summary in pairs[articleList[x]]:
        summary_text = dict[summary][0]
        fragments = Fragments(summary_text, text)
        densities.append(fragments.density())
        coverages.append(fragments.coverage())
        compressions.append(fragments.compression())
    return (x, (densities, coverages, compressions))
def main():
    values = {}
    pbar = tqdm(total=len(articleList), desc='Analyzing:')
    with Pool(processes=15) as pool:
        for results in pool.imap_unordered(analyzeArticle, range(len(articleList))):
            values[articleList[results[0]]] = results[1]
            pbar.update(1)
    with open('../clustering/fragmentStats.json', 'w+') as file:
        json.dump(values, file)

if __name__ == '__main__':
    main()
