import json
with open('../clustering/articleSummaryPairsFinal.json') as f:
    articles = json.load(f)

dumplist = []
for i in range(10):
    dumplist.append(articles)

with open('../clustering/sample.json', 'w+') as f:
    json.dump(dumplist, f)
