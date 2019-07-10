import pprint
import jsonl

def read_clusters():
    pp = pprint.PrettyPrinter()
    fileName = '../clustering/final_clusters_0.9_cleaned.jsonl'
    with jsonl.open(fileName) as file:
        clusters = file.read()
    count = 0
    for cluster in clusters:
        print('cluster '+str(count)+':')
        pp.pprint(cluster)
        count += 1

if __name__ == '__main__':
    read_clusters()
