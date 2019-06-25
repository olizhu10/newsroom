import jsonl
import sys

def length():
    with open("test.json", 'r') as file:
        data = json.load(file)
        print(len(data))

def main():
    #insert links of articles you want to add to jsonl file in this list
    links = ["https://web.archive.org/web/2016061319id_/https://www.washingtonpost.com/national/the-scene-after-a-gunman-opened-fire-at-an-orlando-nightclub/2016/06/12/dd88556a-30a3-11e6-8ff7-7b6c1998b7a0_gallery.html"]
    #enter name of event/file name you want to write to here
    event = "test"
    fileName = "../jsonl_files/"+event+".jsonl"

    for link in links:
        path = "../dataset_files/train.jsonl.gz"
        data = []
        article = {}
        with jsonl.open(path, gzip = True) as train_file:
            train = train_file.read()
            for ln in train:
                if ln['archive'] == link:
                    article = ln
                    data.append(article)
                    break

        try:
            with jsonl.open(fileName) as file:
                file.appendline(article)
        except:
            with open(fileName, 'w+') as file:
                file.appendline(article)

if __name__ == '__main__':
    main()
