import jsonl
import json
import re
import nltk
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
import gensim.downloader as api
from gensim.models import TfidfModel
from gensim.corpora import Dictionary

def run():
    with jsonl.open('../dataset_files/train.jsonl.gz', gzip = True) as file:
        data = file.read()
    articles = [] #remove
    texts = []
    print('beginning preprocessing')
    for article in data:
        #change to write full
        if article["date"] >= str(20160610000000) and article["date"] <= str(20160617000000): #remove
            articles.append(article) #remove
            text = preprocess(article['text'])
            texts.append(text)
    print('finished preprocessing')
    print('begin creating dictionary')
    dict = create_dictionary(articles)
    print('finished creating dictionary')
    print('finding tfidf vectors')
    vectors = tfidf(texts, dict)
    print('found tfidf vectors')
    print('writing identifier')
    write_identifier(articles, vectors)
    print('finished writing identifier')

def write_identifier(articles, vectors):
    """
    Returns dictionary with archive urls of articles as keys and tf-idf vectors as values
    articles: list of articles in the window (dictionaries)
    vectors: list of tfidf vectors generated from articles in the window
    """

    try:
        with open('../clustering/test_identifier.json', 'r') as file:
            dict = json.load(file)
        for x in range(len(articles)):
            dict[articles[x]['archive']] = vectors[x]
        json.dump(dict,'../clustering/identifier.json')
    except:
        dict = {}
        for x in range(len(articles)):
            dict[articles[x]['archive']] = vectors[x]
        with open('../clustering/test_identifier.json', 'w+') as file:
            json.dump(dict,file)

def get_identifier():
    with open('../clustering/identifier.json', 'r') as file:
        dict = json.load(file)
    return dict

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
    intab = '‘’“!"%&()*+,-./:;<=>?#@[\\]^_`{|}~”'
    outtab = '                                  '
    trantab = str.maketrans(intab, outtab)

    return words.translate(trantab)

def lemmatize_stem(words):
    stemmer = SnowballStemmer('english', ignore_stopwords = True)
    lemmatizer = WordNetLemmatizer()
    finished_words = []
    for word in words:
        lemmatized = lemmatizer.lemmatize(word)
        finished_words.append(stemmer.stem(lemmatized))

    return finished_words

def preprocess(s):
    s = remove_punc(s)
    s = s.lower()
    s = re.sub('\s+',' ',s)
    s = s.rstrip(' ')
    s = s.lstrip(' ')
    s = s.split(' ')
    s = lemmatize_stem(s)
    return s

if __name__ == '__main__':
    run()
