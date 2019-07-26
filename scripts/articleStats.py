from statistics import mean, median, stdev
import json
from fragments import Fragments
import csv
from tqdm import tqdm
from multiprocessing import Pool
import jsonl
with open('../clustering/articleSummaryPairsMinLength.json', 'r') as file:
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
    compressions = [articleList[x]]
    densities = [articleList[x]]
    coverages = [articleList[x]]
    text = dict[articleList[x]][1]
    for summary in pairs[articleList[x]]:
        summary_text = dict[summary][0]
        fragments = Fragments(summary_text, text)
        densities.append(fragments.density())
        coverages.append(fragments.coverage())
        compressions.append(fragments.compression())
    return (densities, coverages, compressions)
def main():
    '''densityMeans = []
    densityStds = []
    coverageMeans = []
    coverageStds = []
    compressionMeans = []
    compressionStds = []'''
    densityFile = open('densities.csv', 'a')
    compressionFile = open('compressions.csv', 'a')
    coverageFile = open('coverages.csv', 'a')
    densityWriter = csv.writer(densityFile)
    compressionWriter = csv.writer(compressionFile)
    coverageWriter = csv.writer(coverageFile)
    pbar = tqdm(total=len(articlelist), desc='Analyzing:')
    for results in pool.imap_unordered(analyzeArticle, range(len(articleList))):
        densityWriter.writerow(results[0])
        coverageWriter.writerow(results[1])
        compressionWriter.writerow(results[2])
        '''densityMeans.append(mean(densities))
        compressionMeans.append(mean(compressions))
        coverageMeans.append(mean(coverages))
        densityStds.append(stdev(densities))
        compressionStds.append(stdev(compressions))
        coverageStds.append(stdev(coverages))'''
        pbar.update(1)
    densityFile.close()
    compressionFile.close()
    coverageFile.close()
    '''print("Average Density Standard Deviation:" + str(mean(densityStds)))
    print("Average Compression Standard Deviation:" + str(mean(compressionStds)))
    print("Average Coverage Standard Deviation:" + str(mean(coverageStds)))'''

if __name__ == '__main__':
    main()
