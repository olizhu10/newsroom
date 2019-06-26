import jsonl
import json
import re
import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
import gensim.downloader as api
from gensim.models import TfidfModel
from gensim.corpora import Dictionary

def run():
    with jsonl.open('../events/Orlando.jsonl') as file:
        data = file.read()
    dataset = []
    for article in data:
        text = preprocess(article['text'])
        dataset.append(text)
    dict = Dictionary.load_from_text('../clustering/fullDict.txt')
    vectors = tfidf(dataset, dict)
    identifier(data, vectors)

def write_identifier(articles, vectors):
    """
    Returns dictionary with archive urls of articles as keys and tf-idf vectors as values
    articles: list of articles in the window (dictionaries)
    vectors: list of tfidf vectors generated from articles in the window
    """

    try:
        dict = json.load('../clustering/identifier.json')
        for x in range(len(articles)):
            dict[articles[x]['archive']] = vectors[x]
        json.dump(dict,'../clustering/identifier.json')
    except:
        dict = {}
        for x in range(len(articles)):
            dict[articles[x]['archive']] = vectors[x]
        with open('../clustering/identifier.json', 'w+') as file:
            json.dump(dict,file)

def get_identifier():
    file = open('../clustering/identifier.json', 'r')
    return file

def tfidf(dataset, dct):
    """
    Returns list of tf-idf vectors representing each article in dataset.
    """

    #dct = create_dictionary()
    corpus = [dct.doc2bow(line) for line in dataset]  # convert corpus to BoW format
    model = TfidfModel(corpus)  # fit model
    vectors = []
    for x in range(len(dataset)):
        vectors.append(model[corpus[x]])

    return vectors

def create_dictionary(dataset):
    path = '../dataset_files/train.jsonl.gz'
    with jsonl.open(path, gzip=True) as file:
        dataset = file.read()
    dict = Dictionary([])
    for article in dataset:
        text = preprocess(article['text'])
        dict.add_documents([text])
    dict.save_as_text('../dataset_files/test.txt')

    return dict

def filter_stopwords(words):
    stop_words = set(stopwords.words('english'))
    filtered_words = []
    for word in words:
        if word not in stop_words:
            filtered_words.append(word)

    return filtered_words

def remove_punc(words):
    intab = '‘’“!"%&()*+,-./:;<=>?@[\\]^_`{|}~”'
    outtab = '                                 '
    trantab = str.maketrans(intab, outtab)

    return words.translate(trantab)

def lemmatize_stem(words):
    ps = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    finished_words = []
    for word in words:
        lemmatized = lemmatizer.lemmatize(word)
        finished_words.append(ps.stem(lemmatized))

    return finished_words

def preprocess(s):
    s = remove_punc(s)
    s = s.lower()
    s = re.sub('\s+',' ',s)
    s = s.rstrip(' ')
    s = s.lstrip(' ')
    s = s.split(' ')
    s = filter_stopwords(s)
    s = lemmatize_stem(s)
    return s

if __name__ == '__main__':
    run()
