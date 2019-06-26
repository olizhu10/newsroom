import jsonl
import sklearn
from tfidf_calc import tfidf, preprocess, get_identifier
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
from scipy.sparse import *
from scipy import *
import gensim.downloader as api
from gensim.models import TfidfModel
from gensim.corpora import Dictionary

def window(start, end):
    """
    Returns set of article texts within specified start and end time.

    start and end must be integers of format YYYYMMDDHHMMSS
    """

    path = '../dataset_files/train.jsonl.gz'
    with jsonl.open(path, gzip=True) as file:
        data = file.read()

    dataset = []
    for article in data:
        time = article['date']
        if time >= start and time <= end:
            dataset.append(article['archive'])
        if time > end:
            break

    return dataset

def update_time(original, add):
    """
    original: string representing the original time of format YYYYMMDDHHMMSS
    add: positive int, amount of days to add
    """

    og_year = int(original[:4])
    og_month = int(original[4:6])
    og_day = int(original[6:8])

    new_year = og_year
    new_month = og_month
    new_day = og_day+add

    if og_month in [1,3,5,7,8,10]:
        if new_day > 31:
            new_month = og_month+1
            new_day = new_day-31
    elif og_month in [1,4,6,9,11]:
        if new_day > 30:
            new_month = og_month+1
            new_day = new_day-30
    elif og_month == 12:
        if new_day > 31:
            new_month = 1
            new_day = new_day - 31
            new_year = og_year+1
    else:
        if og_year % 4 == 0 and ((not og_year % 100 == 0) or og_year % 400 == 0):
            if new_day > 29:
                new_month = 3
                new_day = new_day-29
        else:
            if new_day > 28:
                new_month = 3
                new_day = new_day-28

    if new_month < 10:
        new_month = '0'+str(new_month)
    if new_day < 10:
        new_day = '0'+str(new_day)

    return str(new_year)+new_month+new_day+'000000'

def eps(dataset):
    nbrs = NearestNeighbors(n_neighbors=4).fit(dataset)
    distances, indices = nbrs.kneighbors(dataset)
    distanceDec = sorted(distances, reverse=True)
    plt.plot(list(range(1,4+1)), distanceDec)
    plt.show()

'''totalWords should be dictionary length'''
def get_tfidf(archives, totalWords):
    identifier = get_identifier()
    dataList = []
    rowList = []
    colList = []
    for archive in archives:
        for ind, pair in enum(identifier[archive], start = 0):
            dataList.append(pair[1])
            colList.append(pair[0]-1)
            rowList.append(ind)
    '''hardcoded, change as needed'''
    return csr_matrix( (array(dataList),(array(rowList),array(colList))), shape=(len(archives), totalWords) )

def cluster():
    start = 19970101000000
    end = update_time(start,3)
    archives = window(start, end)
    dict = Dictionary.load_from_text('../clustering/fullDict.txt')
    data = get_texts(articles)

    identifier(dataset, vectors)


if __name__ == '__main__':
    with jsonl.open('../events/Orlando.jsonl') as file:
        data = file.read()
    dataset = []
    for article in data:
        text = preprocess(article['text'])
        dataset.append(text)
    dict = Dictionary.load_from_text('../clustering/fullDict.txt')
    vectors = tfidf(dataset,dict)

    eps([dataset])
