import json, gzip
import pprint

path = "../dataset_files/train.jsonl.gz"
data = []
pp = pprint.PrettyPrinter(depth=4)
with gzip.open(path) as f:
    for ln in f:
        obj = json.loads(ln)
        if (obj["date"] >= str(20131205000000) and obj["date"] <= str(20131207000000)
            and ("Mandela" in obj["title"])):

            info = {
                'title': obj["title"],
                'summary': obj["summary"],
                'url': obj['url'],
                'date': obj['date'],
                'archive': obj['archive']
            }
            data.append(info)
            pp.pprint(info)

print(len(data))
