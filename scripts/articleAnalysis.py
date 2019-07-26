from statistics import mean, median, stdev
import json
from fragments import Fragments
import csv
from tqdm import tqdm
from multiprocessing import Pool
import jsonl
with open('../clustering/fragmentStats.json', 'r') as file:
    articles = json.load(file)

def main():
    densityMeans = []
    densityStds = []
    coverageMeans = []
    coverageStds = []
    compressionMeans = []
    compressionStds = []
    pbar = tqdm(total=len(articles), desc='Analyzing:')
    for article in articles:
        densities = articles[article][0]
        coverages = articles[article][1]
        compressions = articles[article][2]
        densityMeans.append(mean(densities))
        compressionMeans.append(mean(compressions))
        coverageMeans.append(mean(coverages))
        densityStds.append(stdev(densities))
        compressionStds.append(stdev(compressions))
        coverageStds.append(stdev(coverages))
        pbar.update(1)
    print("Average Density Standard Deviation:" + str(mean(densityStds)))
    print("Average Compression Standard Deviation:" + str(mean(compressionStds)))
    print("Average Coverage Standard Deviation:" + str(mean(coverageStds)))

if __name__ == '__main__':
    main()
