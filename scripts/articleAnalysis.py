from statistics import mean, median, stdev
import json
from fragments import Fragments
import csv
from tqdm import tqdm
from multiprocessing import Pool
import jsonl

"""
Prints statistics for densities, coverages and compressions of the articles.
"""

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
        densities = list(map(float, densities))
        coverages = articles[article][1]
        coverages = list(map(float, coverages))
        compressions = articles[article][2]
        compressions = list(map(float, compressions))
        densityMeans.append(mean(densities))
        compressionMeans.append(mean(compressions))
        coverageMeans.append(mean(coverages))
        densityStds.append(stdev(densities))
        compressionStds.append(stdev(compressions))
        coverageStds.append(stdev(coverages))
        pbar.update(1)
    print("Average Density Standard Deviation:" + str(mean(densityStds)))
    print("Average Density:" + str(mean(densityMeans)))
    print("Average Compression Standard Deviation:" + str(mean(compressionStds)))
    print("Average Compression:" + str(mean(compressionMeans)))
    print("Average Coverage Standard Deviation:" + str(mean(coverageStds)))
    print("Average Coverage:" + str(mean(coverageMeans)))

if __name__ == '__main__':
    main()
