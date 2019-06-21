import json, gzip
import sys
def length():
    with open("Mandela.json", 'r') as file:
        data = json.load(file)
        print(len(data))

def main():
    links = ["https://web.archive.org/web/2016061219id_/http://www.cnn.com/2016/06/12/us/gallery/orlando-shooting/index.html"]
    event = "Orlando"
    for link in links:
        path = "train.jsonl.gz"
        data = []
        article = {}
        with gzip.open(path) as f:
            for ln in f:
                obj = json.loads(ln)
                if obj['archive'] == link:
                    #print(obj['archive'])
                    article = obj
                    data.append(article)
        #print(data[0])
        fileName = event+".json"

        try:
            with open(fileName, 'r') as file:
                datastore = json.load(file)
                datastore.append(article)
                file = open(fileName, "w")
                json.dump(datastore, file)
        except:
            print('in except')
            file = open(fileName, "w+")
            json.dump(data, file)

if __name__ == '__main__':
    main()
