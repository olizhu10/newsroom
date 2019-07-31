import pprint
import jsonl

def read_clusters():
    pp = pprint.PrettyPrinter()
    fileName = '../clustering/cluster_pairings.jsonl'
    with jsonl.open(fileName) as file:
        clusters = file.read()
    count = 0
    num = 0
    for cluster in clusters:
        num += len(list(cluster.keys()))
        count += 1
    print(num)

if __name__ == '__main__':
    read_clusters()
