from tqdm import tqdm
import spacy
import wmd
import csv
from metric_analysis import CLUSTERS

"""Creates a csv file with wmd scores between summaries in a cluster"""

nlp = spacy.load('en_core_web_lg', create_pipeline=wmd.WMD.create_spacy_pipeline)

def wmd(cluster):
    matrix = []
    for summary1 in cluster:
        doc1 = nlp(summary1)
        wmd_scores = []
        for summary2 in cluster:
            doc2 = nlp(summary2)
            wmd_scores.append(doc1.similarity(doc2))
        matrix.append(wmd_scores)
    return matrix

def main():
    for key in CLUSTERS:
        matrix = wmd(CLUSTERS[key])
        with open('../data/wmd_'+key+'.csv', 'w+') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for row in matrix:
                writer.writerow(row)

if __name__ == '__main__':
    main()
