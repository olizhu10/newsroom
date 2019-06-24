import sys
import jsonl
from ASData import ASData
from fragments import Fragments

"""Creates matrix of article-summary pairs stored as ASData objects"""
def data_matrix():
    #enter name of event (string)
    event="Orlando"
    path = "../jsonl_files/"+event+".jsonl"
    with jsonl.open(path, gzip = False) as train_file:
        articles = train_file.read()

    summaries = []
    for article in articles:
        summaries.append(article['summary'])

    # Compute stats on random training example:
    #article_str = sys.argv[2]
    #article_list = article_str.split()

    summary_lists = [[0,2,3],
                    [0,1,3,6,7,8],
                    [1,2,3,6,7],
                    [0,2,3,4,7,8,9,10],
                    [0,2,3,4,7,8],
                    [1,3,4,5,8],
                    [0,2,3,4,6,7],
                    [0,2,3,4,7,8,9,10],
                    [3,8],
                    [0,2,3,4,7,8,9,10],
                    [0,2,9,10]]
    matrix = []
    num = 0
    for article in articles:
        text = article['text']
        entries = []
        for index in range(len(summaries)):
            summary = summaries[index]
            if index in summary_lists[num]:
                #print('in if')
                fragments = Fragments(summary, text)
                obj = ASData(article, summary, True, fragments.coverage(), fragments.density(), fragments.compression())
                entries.append(obj)
            else:
                #print('in else')
                obj = ASData(article, summary, False)
                entries.append(obj)
        matrix.append(entries)
        num += 1

    return matrix


"""for article in article_list:
    summary = train[summary_num]['summary']
    text = train[int(article)]['text']
    fragments = Fragments(summary, text)

    # Print paper metrics:
    print('For summary '+str(summary_num)+', article '+str(article))
    print("Coverage:",    fragments.coverage())
    print("Density:",     fragments.density())
    print("Compression:", fragments.compression())

    # Extractive fragments oracle:

    print("List of extractive fragments:")
    print(fragments.strings())
"""
if __name__ == '__main__':
    print(data_matrix())
