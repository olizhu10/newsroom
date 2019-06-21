import json, gzip
import pprint

path = "train.jsonl.gz"
data = []
pp = pprint.PrettyPrinter(depth=4)
with gzip.open(path) as f:
    for ln in f:
        obj = json.loads(ln)
        if (obj["date"] >= str(20160612000000) and obj["date"] <= str(20160614000000)
            and "Tony" not in obj['title']
            and "Trump" not in obj['title']
            and ("Orlando" in obj["title"]
            or "shooting" in obj['title'])):

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
