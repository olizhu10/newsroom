import smd
import csv
import pprint
from metric_analysis import CLUSTERS

"""Creates a csv file with s+wms scores between summaries in a cluster"""

def write_file():
    for key in CLUSTERS:
        with open('../data/sms_input_'+key+'.tsv', 'w+') as tsvfile:
            writer = csv.writer(tsvfile, delimiter='\t')
            for summary1 in CLUSTERS[key]:
                for summary2 in CLUSTERS[key]:
                    row = [summary1, summary2]
                    writer.writerow(row)

def wsms(key):
    matrix = []
    with open('../data/sms_input_'+key+'_glove_s+wms.out') as f:
        reader = list(csv.reader(f, delimiter='\t'))
        line = 2
        for summary in range(len(CLUSTERS[key])):
            scores = []
            for x in range(len(CLUSTERS[key])):
                scores.append(float(reader[line][3]))
                line += 1
            matrix.append(scores)
    return matrix

def main():
    for key in CLUSTERS:
        matrix = wsms(key)
        with open('../data/wsms_'+key+'.csv', 'w+') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for row in matrix:
                writer.writerow(row)

if __name__ == '__main__':
    main()
