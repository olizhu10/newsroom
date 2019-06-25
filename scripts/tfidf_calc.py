import jsonl
import re
import nltk
from nltk.corpus import stopwords
import gensim.downloader as api
from gensim.models import TfidfModel
from gensim.corpora import Dictionary

def create_dictionary():
    path = '../dataset_files/train.jsonl.gz'
    with jsonl.open('../events/Orlando.jsonl', gzip=False) as file:
        dataset = file.read()
    dict = Dictionary([])
    for article in dataset:
        text = preprocess(article['text'])
        dict.add_documents([text])
    with jsonl.open('../dataset_files/test.jsonl') as dict_file:
        dict_file.write(dict)
    return dict

def filter_stopwords(words):
    stop_words = set(stopwords.words('english'))
    filtered_words = []
    for word in words:
        if word not in stop_words:
            filtered_words.append(word)
    return filtered_words

def remove_punc(words):
    intab = '[‘’“!"%&()*+,-./:;<=>?@[\\]^_`{|}~]”'
    outtab = '                                   '
    trantab = str.maketrans(intab, outtab)
    return words.translate(trantab)

def preprocess(s):
    s = remove_punc(s)
    s = s.lower()
    s = re.sub('\s+',' ',s)
    s = s.rstrip(' ')
    s = s.lstrip(' ')
    s = s.split(' ')
    s = filter_stopwords(s)
    return s

if __name__ == '__main__':
    create_dictionary()
