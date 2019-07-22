import nltk

from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent

def main():
    ex = 'google gets Sued by Facebook'
    for word in preprocess(ex):
        if word[1]=="NNP":
            print(word[0])

if __name__ == '__main__':
    main()
